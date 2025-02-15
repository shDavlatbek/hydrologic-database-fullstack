# You can import routers from files like this
from api.users import router as router_users
from api.auth import router as router_auth
from api.common import router as router_common
from api.geo import router as router_geo
from api.melio import router as router_melio

all_routers = [
    # Add imported routers
    router_users,
    router_auth,
    router_common,
    router_geo,
    router_melio
]
