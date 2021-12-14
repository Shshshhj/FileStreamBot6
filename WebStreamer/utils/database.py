# (c) @AbirHasan2005

import datetime
import motor.motor_asyncio


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.black = self.db.blacklist
        self.beta = self.db.beta

# ----------------------add ,check or remove user----------------------
    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat()
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    async def remove_user(self, id):
        await self.col.delete_one({'id': int(id)})

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

# ----------------------ban, check banned or unban user----------------------
    def black_user(self, id):
        return dict(
            id=id,
            ban_date=datetime.date.today().isoformat()
        )

    async def ban_user(self, id):
        user = self.black_user(id)
        await self.black.insert_one(user)

    async def unban_user(self, id):
        await self.black.delete_one({'id': int(id)})

    async def is_user_banned(self, id):
        user = await self.black.find_one({'id': int(id)})
        return True if user else False

    async def total_banned_users_count(self):
        count = await self.black.count_documents({})
        return count

# ----------------------Add or remove user from Beta----------------------

    def beta_user(self, id):
        return dict(
            id=id,
            beta_join_date=datetime.date.today().isoformat()
        )

    async def add_user_beta(self, id):
        user = self.beta_user(id)
        await self.beta.insert_one(user)

    async def remove_user_beta(self, id):
        await self.beta.delete_one({'id': int(id)})

    async def is_user_in_beta(self, id):
        user = await self.beta.find_one({'id': int(id)})
        return True if user else False

    async def total_beta_users_count(self):
        count = await self.beta.count_documents({})
        return count