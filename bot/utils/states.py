from aiogram.fsm.state import StatesGroup, State

class Register(StatesGroup):
    
    userId = State()
    firstName = State()
    lastName = State()
    phoneNumber = State()
    userPhoto = State()
    location = State()

class Refresh(StatesGroup):
    
    get = State()
    
class Checkout(StatesGroup):
    
    from_cart = State()
    directly = State()
class RegisterDelivery(StatesGroup):
    
    userId = State()
    firstName = State()
    lastName = State()
    phoneNumber = State()
    userPhoto = State()
    location = State()

class Shop(StatesGroup):
    shopping = State()
    cancel_shoping = State()

    
class ShopItem(StatesGroup):
    selectItem = State()
    unselectItem = State()
    choosingItems = State()
