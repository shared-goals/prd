# Shared Goals — Спецификация моделей данных

**Версия:** 0.1 (черновик)
**Дата:** 2026-02-16
**Автор:** Shago (на основе Текста p2-180 и архитектуры SOSenki)

---

## Источники

Модели основаны на 4 сущностях из [p2-180-sharedgoals](https://text.sharedgoals.ru/p2-180-sharedgoals/):
Цель, Контракт, Исполнение (Commit), План действий.

Архитектурный паттерн — из SOSenki: SQLAlchemy + Alembic + FastAPI + Telegram.

## Принципы (из Текста)

1. **Без сравнительных метрик между людьми.** Нет рейтингов, лидербордов, "кто больше". Социальный капитал — агрегированный, не персональный.
2. **Без манипулятивной геймификации.** Вовлекать, но не создавать зависимость.
3. **Растворена в привычных каналах.** Telegram-first. Не "ещё одна система".
4. **Контракт = время, которое готов тратить.** Без напоминалок и будильников.
5. **Commit = "что сделал" + "следующий шаг".** Опциональный флаг момента счастья.
6. **Open Source, MIT.** Всё открыто.
7. **Фокус на МЫ, не на Я.** Цели неконкурентные, гуманистические.

---

## Модели

### User

Переиспользуем паттерн из SOSenki. Минимальная модель пользователя через Telegram.

```python
class User(Base, BaseModel):
    """Участник платформы. Идентификация через Telegram."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        unique=True, nullable=False, index=True,
        comment="Telegram user ID — primary identity",
    )
    username: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="Telegram @username",
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Display name (from Telegram or self-set)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False,
    )
    timezone: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment="IANA timezone (e.g., Europe/Moscow)",
    )
```

**Заметки:**
- Нет ролей admin/staff — на MVP все равны. Администрирование через `access.admin_telegram_ids` (как в thunder-forge).
- Нет аватаров, бейджей, уровней — принцип "без сравнительных метрик".

---

### Goal (Цель)

> «Неконкурентная, гуманистическая цель в "евангельской системе координат": благородное любопытство + любовь без долженствования + человек как образ Бога + цели больше жизни.»

```python
class GoalVisibility(str, Enum):
    PUBLIC = "public"       # В каталоге, по QR, по геолокации
    INVITE = "invite"       # Только по ссылке/приглашению
    PERSONAL = "personal"   # Только автор


class GoalStatus(str, Enum):
    ACTIVE = "active"       # Цель жива, принимает участников
    PAUSED = "paused"       # Автор приостановил
    COMPLETED = "completed" # Достигнута (или закрыта осознанно)


class Goal(Base, BaseModel):
    """Общая цель — направление движения, не точка назначения.

    Это скорее "Люблю программировать", чем "Написать программу".
    Образ идеального состояния, к которому стремишься.
    """

    __tablename__ = "goals"

    # Автор цели
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True,
        comment="Кто сформулировал цель",
    )

    # Содержание
    title: Mapped[str] = mapped_column(
        String(500), nullable=False,
        comment="Краткая формулировка цели",
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Развёрнутое описание: зачем, почему, какой образ счастья за ней стоит",
    )

    # Видимость
    visibility: Mapped[GoalVisibility] = mapped_column(
        default=GoalVisibility.PUBLIC, nullable=False, index=True,
        comment="public — в каталоге; invite — по ссылке; personal — только автор",
    )

    # Статус
    status: Mapped[GoalStatus] = mapped_column(
        default=GoalStatus.ACTIVE, nullable=False, index=True,
    )

    # Опциональная привязка
    text_url: Mapped[str | None] = mapped_column(
        String(1000), nullable=True,
        comment="Ссылка на главу Текста или внешний ресурс, описывающий контекст цели",
    )

    # Relationships
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    contracts: Mapped[list["Contract"]] = relationship(
        "Contract", back_populates="goal", cascade="all, delete-orphan",
    )
```

**Заметки:**
- Нет категорий/тегов на MVP — усложняет без необходимости.
- `text_url` — мост между Текстом и Платформой. Цель может быть "проиллюстрирована" главой.
- Нет `is_public` / `visibility` — все цели открыты (принцип Open Source).
- Нет `parent_id` / иерархии — YAGNI.

---

### Contract (Контракт)

> «Время, которое готов тратить. 1 час/неделю, 20 мин/месяц. Без напоминалок и будильников.»

```python
class ContractCadence(str, Enum):
    """Как часто участник готов вкладываться."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    OCCASIONALLY = "occasionally"  # без регулярности, по вдохновению


class Contract(Base, BaseModel):
    """Контракт — обязательство участника перед целью.

    Не юридический контракт. Это данное себе слово (как в "Шиле в Ж...":
    видишь, что другой занятой человек исполняет — сам исполняешь).
    """

    __tablename__ = "contracts"

    # Связи
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True,
    )
    goal_id: Mapped[int] = mapped_column(
        ForeignKey("goals.id"), nullable=False, index=True,
    )

    # Обязательство
    cadence: Mapped[ContractCadence] = mapped_column(
        default=ContractCadence.WEEKLY, nullable=False,
        comment="Регулярность: как часто готов вкладываться",
    )
    time_minutes: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="Сколько минут за период готов потратить (необязательно, без давления)",
    )

    # Состояние
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False,
        comment="Активен ли контракт (можно приостановить без удаления)",
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    goal: Mapped["Goal"] = relationship("Goal", back_populates="contracts")
    commits: Mapped[list["Commit"]] = relationship(
        "Commit", back_populates="contract", cascade="all, delete-orphan",
    )

    __table_args__ = (
        # Один активный контракт на пару user+goal
        Index("idx_contract_user_goal", "user_id", "goal_id"),
    )
```

**Заметки:**
- `time_minutes` опционален — принцип "без долженствования".
- Нет прогресс-баров, процентов выполнения, streak-счётчиков.
- Деактивация через `is_active=False`, не удаление (история сохраняется).

---

### Commit (Исполнение)

> «"Что было сделано" + "Следующий шаг" + опциональный флаг момента счастья + фото/место/человек.»

```python
class Commit(Base, BaseModel):
    """Исполнение — фиксация того, что сделано.

    Аналогия с Git commit: атомарная единица прогресса.
    Не отчёт, а рефлексия: что сделал и что дальше.
    """

    __tablename__ = "commits"

    # Связь с контрактом (и через него — с целью и пользователем)
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id"), nullable=False, index=True,
    )

    # Содержание
    what_done: Mapped[str] = mapped_column(
        Text, nullable=False,
        comment="Что было сделано",
    )
    next_step: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Следующий шаг (необязательно)",
    )

    # Анонимность
    is_public: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
        comment="Автор явно делает коммит публичным (по умолчанию анонимен — виден только агрегат)",
    )

    # Момент счастья
    is_happy_moment: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
        comment="Флаг: это был момент счастья?",
    )

    # Опциональные метаданные
    photo_url: Mapped[str | None] = mapped_column(
        String(1000), nullable=True,
        comment="Фото (ссылка или Telegram file_id)",
    )
    location: Mapped[str | None] = mapped_column(
        String(500), nullable=True,
        comment="Место (свободный текст или координаты)",
    )
    with_person: Mapped[str | None] = mapped_column(
        String(500), nullable=True,
        comment="С кем (имя, без привязки к User — может быть не на платформе)",
    )

    # Время, потраченное на это действие
    time_spent_minutes: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="Сколько минут потрачено (для социального капитала, необязательно)",
    )

    # Relationships
    contract: Mapped["Contract"] = relationship("Contract", back_populates="commits")

    __table_args__ = (
        Index("idx_commit_contract_created", "contract_id", "created_at"),
    )
```

**Заметки:**
- `is_happy_moment` — ключевая метрика всей платформы. Не "оценка" (1-5), а бинарный флаг: был момент счастья или нет.
- `time_spent_minutes` — входные данные для социального капитала. Но опциональны (принцип "без давления").
- `with_person` — свободный текст, не FK. Человек, с которым ты был счастлив, может быть не на платформе.
- Нет лайков, комментариев, шеров. Commit — личная рефлексия, не пост в соцсети.

---

### ActionPlan (План действий)

> «Опционально, потенциал для монетизации (эксперты предлагают планы с услугами).»

```python
class ActionPlan(Base, BaseModel):
    """План действий — опциональная структура шагов к цели.

    На MVP — простой текстовый план. В будущем — потенциал для
    экспертных планов (монетизация через услуги).
    """

    __tablename__ = "action_plans"

    # Связь
    goal_id: Mapped[int] = mapped_column(
        ForeignKey("goals.id"), nullable=False, index=True,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True,
        comment="Автор плана (может отличаться от автора цели)",
    )

    # Содержание
    title: Mapped[str] = mapped_column(
        String(500), nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
        comment="Markdown-текст плана",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False,
    )

    # Relationships
    goal: Mapped["Goal"] = relationship("Goal")
    author: Mapped["User"] = relationship("User")
```

**Заметки:**
- На MVP — placeholder. Текстовое поле, не дерево задач.
- Разные люди могут предложить разные планы к одной цели (Fork-подход).

---

## Агрегаты (не хранятся, вычисляются)

### Социальный капитал

> «НЕ социальный рейтинг. Без контроля и порицания. = временные инвестиции без ожидания долженствования = цифровая метрика Любви.»

```python
# НЕ модель, а функция
def social_capital(goal_id: int | None = None) -> int:
    """Совокупное время, инвестированное всеми участниками.

    Если goal_id задан — для конкретной цели.
    Если None — для всей платформы.

    Возвращает: общее количество минут.

    Принципиально:
    - Не разбивается по пользователям (нет рейтинга)
    - Не сравнивается между целями (нет конкуренции)
    - Это ОДИН число для всех — интегральный показатель
    """
    # SELECT COALESCE(SUM(time_spent_minutes), 0)
    # FROM commits
    # JOIN contracts ON commits.contract_id = contracts.id
    # WHERE contracts.goal_id = :goal_id (if specified)
    ...
```

### Моменты счастья (агрегат)

```python
def happy_moments_count(goal_id: int | None = None) -> int:
    """Количество коммитов, отмеченных как моменты счастья.

    Тот же принцип: общее число, без персональной разбивки.
    """
    ...
```

---

## Telegram Bot — команды MVP

```
/start          — Приветствие, краткое описание
/goals          — Список активных целей (inline buttons)
/new_goal       — Создать цель (пошаговый диалог)
/join <goal_id> — Присоединиться к цели (создать контракт)
/commit         — Зафиксировать что сделал (пошаговый диалог)
/my             — Мои контракты и последние коммиты
/capital        — Социальный капитал (общее число)
```

Альтернатива: Mini App (как в SOSenki) для визуального интерфейса.

---

## Миграция (Alembic)

Паттерн из SOSenki: `src/migrations/versions/001_initial_schema.py`

---

## Что НЕ входит в MVP

- [ ] Персональные метрики / дашборды
- [ ] Уведомления / напоминалки
- [ ] Геймификация (бейджи, стрики, уровни)
- [ ] Комментарии к коммитам
- [ ] Подписки на чужие цели (кроме join)
- [ ] Монетизация планов действий
- [ ] RAG/MCP интеграция (следующий этап)
- [ ] Multi-language (сначала RU)

---

## Что входит в MVP

- [x] User (Telegram auth)
- [x] Goal (CRUD через бот)
- [x] Contract (join/leave)
- [x] Commit (фиксация + флаг счастья)
- [x] Social Capital (агрегат)
- [x] Telegram бот с базовыми командами
- [x] SQLite (как в SOSenki)
- [x] Alembic миграции
- [x] AuditLog (паттерн из SOSenki)

---

## Куда класть код

**Вариант А:** Новый репозиторий `shared-goals/platform` (чистый старт).

**Вариант Б:** Внутрь `thunder-forge` (уже есть FastAPI + Telegram + auth).

**Рекомендация:** Вариант Б. Thunder-forge задуман как "operational glue" и в README уже описывает архитектуру Shared Goals. Добавить `src/models/`, `src/services/goal_service.py`, `src/bot/handlers/goals.py` — естественное расширение. Когда вырастет — можно выделить.

---

## Решения по открытым вопросам (02.03.2026)

1. **Анонимность коммитов** ✅
   Участники НЕ видят автора коммита по умолчанию. Только агрегаты (социальный капитал, моменты счастья) без привязки к личности. Автор может явно сделать коммит публичным — его выбор.
   → Добавить поле `is_public: bool = False` в модель `Commit`.

2. **Публичность целей** ✅
   Три режима видимости (из Текста p2-180):
   - `public` — в каталоге по ключевым словам, геолокации, QR
   - `invite` — по приглашению/ссылке (закрытый круг)
   - `personal` — только автор (вырожденный сценарий)
   → Добавить поле `visibility: GoalVisibility` в модель `Goal`. Убрать заметку "все цели открыты".

3. **Telegram группы** ✅
   Цель — самостоятельная сущность платформы с ключом/ссылкой. Привязки к группе нет. Ею можно поделиться где угодно — в группе, канале, в личке, через QR. Это задача клиента, не платформы.

4. **Связь с Текстом** ✅
   Участники ведут свои тексты на платформе (text-forge) и раскрывают там цели и мотивы — это важный элемент экосистемы. `text_url` в модели `Goal` — правильный подход. Thunder-forge будет управлять агентами, реализующими задачи из Текста (вычислительные мощности Сергея под управлением github.com/shared-goals/thunder-forge).

5. **Где хостить MVP** ✅
   Отдельный Linux VPS. Не рядом с OpenClaw. Можно купить дешёвый VPS специально под MVP. Linux — предпочтительная ОС.
