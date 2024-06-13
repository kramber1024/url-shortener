from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db

SessionDependency = Annotated[AsyncSession, Depends(db.scoped_session_dependency)]
