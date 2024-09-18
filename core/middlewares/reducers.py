from uuid import UUID
from modules.users.repository import UserRepository
from modules.transactions.repository import TransactionRepository, BookRepository

userRepo = UserRepository()
transactionRepo = TransactionRepository()
bookRepo = BookRepository()
 
async def act_on_users(action: str, payload, id: UUID = None):
    match action:
        case "create_user":
            try:
                await userRepo.create(payload=payload)
            
            except Exception as error:
                print(error)
                raise error
            
        case "update_user":
            try:
                await userRepo.partial_update_user_profile(payload=payload, user_id=id)
            
            except Exception as error:
                print(error)
                raise error
    
 
async def act_on_transactions(action: str, payload, id: UUID = None):
    match action:
        case "create_transactions":
            try:
                await transactionRepo.create(payload=payload)
            
            except Exception as error:
                raise error
    
 
async def act_on_books(action: str, payload, id: UUID = None):
    match action:
        case "create_book":
            try:
                await bookRepo.create_book(payload=payload)
            
            except Exception as error:
                raise error
        
        case "update_book":
            try:
                await bookRepo.update_book(payload=payload, book_id=id)
            
            except Exception as error:
                raise error
        
        case "remove_book":
            try:
                await bookRepo.delete_book(book_id=id)
            
            except Exception as error:
                raise error
            
    