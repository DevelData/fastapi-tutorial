from datetime import datetime, timedelta
from typing import Dict
from jose import jwt, JWTError


SECRET_KEY = "bbS4x5rGh5H5oU9R1ZCC4TndPDtZxj2tuJayybFpKzPqKgErjJPZm832K7Qsan2t"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:Dict):
    to_encode = data.copy()
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)