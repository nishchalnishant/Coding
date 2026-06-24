---
tags: [coding, amazon-interview, oop, design-patterns, solid, lld]
topic: OOP & Design Patterns — Amazon SDE-2
difficulty: sde2
---

# OOP & Design Patterns — Amazon SDE-2

> Amazon may ask "design a parking lot" or "design an LRU cache" in a coding or LLD round. OOP concepts come up in system design ("how would you model this?") and behavioral rounds ("how do you approach code organization?"). SOLID principles frequently appear in code review discussions. Know Parking Lot and LRU Cache implementations cold.

---

## SOLID Principles

### S — Single Responsibility Principle
> **One class, one reason to change.**

```python
# BAD: UserManager does too much
class UserManager:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...   # email concern
    def log_user_creation(self, user): ...    # logging concern

# GOOD: each class has one responsibility
class UserService:
    def create_user(self, data): ...

class EmailService:
    def send_welcome_email(self, user): ...

class AuditLogger:
    def log_event(self, event): ...
```

### O — Open/Closed Principle
> **Open for extension, closed for modification.**

```python
# BAD: adding a new shape requires modifying existing code
class AreaCalculator:
    def calculate(self, shape):
        if isinstance(shape, Circle):
            return math.pi * shape.radius ** 2
        elif isinstance(shape, Square):
            return shape.side ** 2
        # Adding Triangle requires modifying this class

# GOOD: extend by adding new classes, not modifying existing ones
class Shape:
    def area(self): raise NotImplementedError

class Circle(Shape):
    def area(self): return math.pi * self.radius ** 2

class Square(Shape):
    def area(self): return self.side ** 2

class Triangle(Shape):        # new shape: no existing code touched
    def area(self): return 0.5 * self.base * self.height

class AreaCalculator:
    def calculate(self, shape: Shape):
        return shape.area()   # works with any Shape
```

### L — Liskov Substitution Principle
> **Subclasses must be usable wherever parent class is expected.**

```python
# BAD: Square breaks Rectangle's contract
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        self.height = w  # breaks Liskov! Square can't honor independent w/h
    def set_height(self, h):
        self.width = h
        self.height = h

# Code that works for Rectangle breaks for Square:
r = Square()
r.set_width(5)
r.set_height(3)
assert r.area() == 15  # FAILS: returns 9 (3×3)

# GOOD: separate abstractions
class Shape: pass
class Rectangle(Shape): ...
class Square(Shape): ...   # doesn't inherit from Rectangle
```

### I — Interface Segregation Principle
> **Many specific interfaces > one general interface.**

```python
# BAD: not all workers can work() AND eat()
class Worker:
    def work(self): ...
    def eat(self): ...

class Robot(Worker):
    def work(self): ...
    def eat(self): raise NotImplementedError("Robots don't eat!")

# GOOD: split into focused interfaces
class Workable:
    def work(self): ...

class Feedable:
    def eat(self): ...

class Human(Workable, Feedable): ...
class Robot(Workable): ...          # only implements what it uses
```

### D — Dependency Inversion Principle
> **Depend on abstractions, not concretions.**

```python
# BAD: high-level module depends on low-level module directly
class NotificationService:
    def __init__(self):
        self.sender = EmailSender()   # tightly coupled

    def notify(self, user, msg):
        self.sender.send(user.email, msg)

# GOOD: depend on an abstraction
class MessageSender:   # abstract
    def send(self, destination, message): raise NotImplementedError

class EmailSender(MessageSender):
    def send(self, destination, message): ...

class SmsSender(MessageSender):
    def send(self, destination, message): ...

class NotificationService:
    def __init__(self, sender: MessageSender):   # injected
        self.sender = sender

    def notify(self, user, msg):
        self.sender.send(user.email, msg)

# Usage:
service = NotificationService(EmailSender())
service = NotificationService(SmsSender())   # swap without touching NotificationService
```

---

## The 8 Must-Know Design Patterns

### 1. Singleton
> Ensure only one instance of a class exists.

```python
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        self.connection = ...  # expensive initialization

# Usage:
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True — same instance

# Thread-safe Singleton (with lock):
import threading
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:   # double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**When to use**: Configuration manager, connection pools, loggers.
**Drawbacks**: Hard to test (global state); violates SRP; hides dependencies.

---

### 2. Factory Method
> Let subclasses decide which class to instantiate.

```python
class Notification:
    def send(self): raise NotImplementedError

class EmailNotification(Notification):
    def send(self): print("Sending email")

class SmsNotification(Notification):
    def send(self): print("Sending SMS")

class PushNotification(Notification):
    def send(self): print("Sending push")

class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        factories = {
            'email': EmailNotification,
            'sms': SmsNotification,
            'push': PushNotification,
        }
        if channel not in factories:
            raise ValueError(f"Unknown channel: {channel}")
        return factories[channel]()

# Usage:
notif = NotificationFactory.create('email')
notif.send()
```

**When to use**: When the exact class to instantiate is determined at runtime.

---

### 3. Observer
> One object changes → all dependents automatically notified.

```python
class EventEmitter:
    def __init__(self):
        self._subscribers: dict[str, list] = {}

    def subscribe(self, event: str, handler):
        self._subscribers.setdefault(event, []).append(handler)

    def emit(self, event: str, data=None):
        for handler in self._subscribers.get(event, []):
            handler(data)

# Usage:
emitter = EventEmitter()

def on_user_created(user):
    print(f"Sending welcome email to {user['email']}")

def on_user_created_log(user):
    print(f"Audit log: user {user['id']} created")

emitter.subscribe('user.created', on_user_created)
emitter.subscribe('user.created', on_user_created_log)

emitter.emit('user.created', {'id': 1, 'email': 'a@b.com'})
# Both handlers fire
```

**When to use**: Event systems, MVC (Model notifies View), real-time updates.

---

### 4. Strategy
> Define a family of algorithms; make them interchangeable at runtime.

```python
from typing import Protocol

class SortStrategy(Protocol):
    def sort(self, data: list) -> list: ...

class QuickSort:
    def sort(self, data): return sorted(data)  # simplified

class MergeSort:
    def sort(self, data): return sorted(data)  # simplified

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)

# Usage:
sorter = Sorter(QuickSort())
sorter.sort([3,1,2])

sorter.set_strategy(MergeSort())   # swap at runtime
sorter.sort([3,1,2])
```

**When to use**: Multiple algorithms for the same problem (payment methods, compression, sorting).

---

### 5. Decorator
> Add behavior to objects dynamically without modifying their class.

```python
class TextProcessor:
    def process(self, text: str) -> str:
        return text

class UppercaseDecorator:
    def __init__(self, processor):
        self._processor = processor

    def process(self, text: str) -> str:
        return self._processor.process(text).upper()

class TrimDecorator:
    def __init__(self, processor):
        self._processor = processor

    def process(self, text: str) -> str:
        return self._processor.process(text).strip()

# Compose decorators:
processor = TrimDecorator(UppercaseDecorator(TextProcessor()))
processor.process("  hello world  ")  # → "HELLO WORLD"
```

**When to use**: Adding cross-cutting concerns (logging, caching, auth) without modifying core logic.

---

### 6. Builder
> Construct complex objects step by step.

```python
class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.toppings = []

class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def size(self, size: str) -> 'PizzaBuilder':
        self._pizza.size = size
        return self

    def crust(self, crust: str) -> 'PizzaBuilder':
        self._pizza.crust = crust
        return self

    def topping(self, topping: str) -> 'PizzaBuilder':
        self._pizza.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        return self._pizza

# Usage:
pizza = (PizzaBuilder()
         .size('large')
         .crust('thin')
         .topping('cheese')
         .topping('mushrooms')
         .build())
```

**When to use**: Constructors with many optional parameters. More readable than telescoping constructors.

---

### 7. Command
> Encapsulate a request as an object (supports undo/redo, queuing).

```python
class Command:
    def execute(self): raise NotImplementedError
    def undo(self): raise NotImplementedError

class TextEditor:
    def __init__(self):
        self.text = ""
        self._history = []

    def execute(self, command: Command):
        command.execute()
        self._history.append(command)

    def undo(self):
        if self._history:
            self._history.pop().undo()

class InsertCommand(Command):
    def __init__(self, editor, text, position):
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self):
        self.editor.text = (self.editor.text[:self.position]
                            + self.text
                            + self.editor.text[self.position:])

    def undo(self):
        end = self.position + len(self.text)
        self.editor.text = self.editor.text[:self.position] + self.editor.text[end:]
```

**When to use**: Text editors, transaction systems, task queues, macro recording.

---

### 8. Adapter
> Make incompatible interfaces work together.

```python
class EuropeanSocket:
    def plug_in(self): return "220V"

class USAppliance:
    def charge(self, socket) -> str:
        return socket.provide_110v()

class SocketAdapter:
    def __init__(self, european_socket: EuropeanSocket):
        self._socket = european_socket

    def provide_110v(self) -> str:
        raw = self._socket.plug_in()  # "220V"
        return self._convert(raw)     # convert to "110V"

    def _convert(self, voltage): return "110V"

# Usage:
appliance = USAppliance()
adapter = SocketAdapter(EuropeanSocket())
appliance.charge(adapter)   # works without modifying either class
```

---

## OOP Interview Problems

### Design a Parking Lot

```python
from enum import Enum
from typing import Optional
import time

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: VehicleType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None

    def can_fit(self, vehicle_type: VehicleType) -> bool:
        return self.spot_type.value >= vehicle_type.value

    def park(self, vehicle) -> bool:
        if self.is_occupied or not self.can_fit(vehicle.vehicle_type):
            return False
        self.is_occupied = True
        self.vehicle = vehicle
        return True

    def unpark(self):
        self.is_occupied = False
        self.vehicle = None

class Vehicle:
    def __init__(self, plate: str, vehicle_type: VehicleType):
        self.plate = plate
        self.vehicle_type = vehicle_type
        self.entry_time = None

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()

class ParkingLot:
    def __init__(self):
        self.spots: list[ParkingSpot] = []
        self.active_tickets: dict[str, Ticket] = {}  # plate → ticket
        self.rate = 2.0  # $/hour

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def find_spot(self, vehicle_type: VehicleType) -> Optional[ParkingSpot]:
        # Prefer smallest fitting spot (motorcycle spot for motorcycle)
        candidates = [s for s in self.spots if not s.is_occupied and s.can_fit(vehicle_type)]
        return min(candidates, key=lambda s: s.spot_type.value, default=None)

    def check_in(self, vehicle: Vehicle) -> Optional[Ticket]:
        spot = self.find_spot(vehicle.vehicle_type)
        if not spot:
            return None  # lot full
        spot.park(vehicle)
        ticket = Ticket(vehicle, spot)
        self.active_tickets[vehicle.plate] = ticket
        return ticket

    def check_out(self, plate: str) -> float:
        ticket = self.active_tickets.pop(plate, None)
        if not ticket:
            return 0.0
        ticket.spot.unpark()
        hours = (time.time() - ticket.entry_time) / 3600
        return round(hours * self.rate, 2)
```

**Interviewer follow-ups:**
- "How would you handle multiple floors?" → Add `floor_id` to ParkingSpot
- "How would you support reservations?" → Add `reserved_until` to ParkingSpot
- "How would you scale this for multiple parking lots?" → ParkingLotManager, database persistence
- "How would you handle payment?" → PaymentStrategy (cash, card, app)

---

### Design a Library Management System

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional

class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"

class Book:
    def __init__(self, isbn: str, title: str, author: str, copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

class Member:
    def __init__(self, member_id: str, name: str):
        self.member_id = member_id
        self.name = name
        self.borrowed_books: list['Loan'] = []
        self.MAX_BOOKS = 5

    def can_borrow(self) -> bool:
        return len(self.borrowed_books) < self.MAX_BOOKS

class Loan:
    LOAN_DAYS = 14

    def __init__(self, book: Book, member: Member):
        self.book = book
        self.member = member
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=self.LOAN_DAYS)
        self.return_date: Optional[datetime] = None

    def is_overdue(self) -> bool:
        return self.return_date is None and datetime.now() > self.due_date

    def fine(self, rate_per_day: float = 0.50) -> float:
        if not self.is_overdue():
            return 0.0
        overdue_days = (datetime.now() - self.due_date).days
        return overdue_days * rate_per_day

class Library:
    def __init__(self):
        self.catalog: dict[str, Book] = {}   # isbn → Book
        self.members: dict[str, Member] = {}  # member_id → Member
        self.active_loans: list[Loan] = []

    def add_book(self, book: Book):
        if book.isbn in self.catalog:
            self.catalog[book.isbn].total_copies += book.total_copies
            self.catalog[book.isbn].available_copies += book.available_copies
        else:
            self.catalog[book.isbn] = book

    def borrow(self, isbn: str, member_id: str) -> Optional[Loan]:
        book = self.catalog.get(isbn)
        member = self.members.get(member_id)
        if not book or not member:
            return None
        if book.available_copies == 0 or not member.can_borrow():
            return None
        book.available_copies -= 1
        loan = Loan(book, member)
        member.borrowed_books.append(loan)
        self.active_loans.append(loan)
        return loan

    def return_book(self, isbn: str, member_id: str) -> float:
        member = self.members.get(member_id)
        book = self.catalog.get(isbn)
        if not member or not book:
            return 0.0
        loan = next((l for l in member.borrowed_books
                     if l.book.isbn == isbn and l.return_date is None), None)
        if not loan:
            return 0.0
        loan.return_date = datetime.now()
        book.available_copies += 1
        member.borrowed_books.remove(loan)
        return loan.fine()
```

---

### Design a Chess Game

```python
from enum import Enum
from typing import Optional, Tuple

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class PieceType(Enum):
    KING = "K"; QUEEN = "Q"; ROOK = "R"
    BISHOP = "B"; KNIGHT = "N"; PAWN = "P"

class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.piece_type = piece_type

    def valid_moves(self, pos, board) -> list[Tuple[int,int]]:
        raise NotImplementedError

class King(Piece):
    def __init__(self, color): super().__init__(color, PieceType.KING)
    def valid_moves(self, pos, board):
        r, c = pos
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        return [(r+dr, c+dc) for dr,dc in dirs
                if 0 <= r+dr < 8 and 0 <= c+dc < 8
                and (board[r+dr][c+dc] is None
                     or board[r+dr][c+dc].color != self.color)]

class Board:
    def __init__(self):
        self.grid: list[list[Optional[Piece]]] = [[None]*8 for _ in range(8)]
        self._setup()

    def _setup(self):
        # Place pieces in starting positions
        for col in range(8):
            self.grid[1][col] = Piece(Color.BLACK, PieceType.PAWN)
            self.grid[6][col] = Piece(Color.WHITE, PieceType.PAWN)
        # ... rooks, knights, bishops, queens, kings

    def move(self, from_pos, to_pos, current_player: Color) -> bool:
        r1, c1 = from_pos
        r2, c2 = to_pos
        piece = self.grid[r1][c1]
        if not piece or piece.color != current_player:
            return False
        if to_pos not in piece.valid_moves(from_pos, self.grid):
            return False
        self.grid[r2][c2] = piece
        self.grid[r1][c1] = None
        return True

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = Color.WHITE
        self.is_over = False

    def make_move(self, from_pos, to_pos) -> bool:
        if self.is_over:
            return False
        success = self.board.move(from_pos, to_pos, self.current_turn)
        if success:
            self.current_turn = (Color.BLACK
                                 if self.current_turn == Color.WHITE
                                 else Color.WHITE)
        return success
```

---

## Key OOP Interview Talking Points

When the interviewer asks "how would you improve this?", say:

1. **"I'd extract this into its own class"** — SRP in action
2. **"I'd use an interface here so we can swap implementations"** — DI + OCP
3. **"I'd use the Observer pattern here so components stay decoupled"** — event-driven design
4. **"I'd make this a Strategy so we can change the algorithm at runtime"** — Strategy pattern
5. **"This constructor has too many parameters — I'd use a Builder"** — readability
6. **"I'd add a Factory here so callers don't need to know which concrete class to instantiate"** — encapsulation

---

## See Also

- [Amazon Interview Strategy](./google-interview-strategy.md)
- [System Design Guide](./system-design.md)
- [Advanced Data Structures](./data-structures/advanced.md) — LRU/LFU implementations
