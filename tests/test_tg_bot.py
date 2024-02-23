import pytest
from unittest.mock import MagicMock
from telegram import Update
from telegram.ext import ContextTypes
from src.tg_bot import access_check

@pytest.mark.asyncio
async def test_access_check_is_true():
    user_list = [123456789]
    update = MagicMock(spec=Update)
    update.effective_user.id = user_list[0]
    result = await access_check(update, ContextTypes.DEFAULT_TYPE, user_list)
    assert result == True

@pytest.mark.asyncio
async def test_access_check_is_false():
    wrong_user_id = 987654321
    user_list = [123456789]
    update = MagicMock(spec=Update)
    update.effective_user.id = wrong_user_id
    result = await access_check(update, ContextTypes.DEFAULT_TYPE, user_list)
    assert result == False
