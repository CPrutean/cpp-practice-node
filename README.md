# cpp-workshop

C++ + Python ROS 2 (Jazzy) workshop workspace. The repo root is the colcon workspace.

```
src/cpp_node_template/   empty C++ node (cpp_node) for you to fill in
src/py_node_template/    finished Python node (py_node), pytest, launch + params
docker/                  Dockerfile (runtime, dev), docker-compose.yml, deps.txt, container.bashrc
.devcontainer/           VS Code "Reopen in Container" config (uses the compose `dev` service)
```

## Quick start

```sh
make test     # build + run unit tests in a clean container
make shell    # interactive dev container
make run      # build and launch the node
```

Inside the container: `cb` (colcon build), `ct` (colcon test), `rs` (re-source), `ros-clean`.

```sh
ros2 launch py_node_template workshop.launch.py   # py_node + cpp_node
ros2 topic echo /py_to_cpp
ros2 topic pub /cpp_to_py std_msgs/msg/String "{data: hi}"
```

## How the nodes talk

Both use `std_msgs/msg/String`:

| topic       | publisher | subscriber |
|-------------|-----------|------------|
| `py_to_cpp` | py_node (`ping <n>`, 1 Hz) | cpp_node (you write this) |
| `cpp_to_py` | cpp_node (you write this)  | py_node (logs it)         |

`cpp_node` currently just spins; add the subscriber and publisher in `src/cpp_node_template/src/main.cpp`.

## Adding a package

Copy `src/cpp_node_template`, rename it in `package.xml`, `CMakeLists.txt` and the launch file, and add any
apt dependencies the build needs to `docker/deps.txt`. For clangd, point `--compile-commands-dir` at
`build/<your_package>` (see `.devcontainer/devcontainer.json`).

## Notes

- The container user is `trickfire` (uid/gid 1000, override with `USER_UID`/`USER_GID`) so bind-mounted
  build output is owned by you on Linux.
- The Dockerfile sets `APT::Sandbox::User "root"` because apt's `_apt` user failed signature checks
  on some Docker Desktop setups.
# cpp-practice-node
