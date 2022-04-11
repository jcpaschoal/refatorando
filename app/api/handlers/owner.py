from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=schemas.AddressResponse)
def add_address(
    address_in: schemas.AddressCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):

    print(current_user)
    
    if current_user is None:
        raise HTTPException(status_code=400, detail="User does not exists")

    address = service.user.add_address(db, address_in)

    return address_in
