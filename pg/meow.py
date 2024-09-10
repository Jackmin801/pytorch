from typing import cast
import torch
import torch.distributed as dist


dist.init_process_group()
rank = dist.get_rank()

# Get default process group?
# Get store
from torch.distributed.distributed_c10d import _world
if rank == 0:
    #print(_world.default_pg)
    #print(_world.pg_map, type(_world.pg_map), len(_world.pg_map), _world.pg_map.keys(), _world.pg_map.values())

    store = _world.pg_map[_world.default_pg][-1]
    while isinstance(store, dist.PrefixStore):
        store = store.underlying_store
    store = cast(dist.TCPStore, store)
    #print(store.set("key", "value"))
    #print(store.add("num", 1))
    print("Num Keys", store.num_keys())

dist.destroy_process_group()

