from src.schemas.facilities import AddFacilities
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: AddFacilities):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return facility
