const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  full_name: state => state.user.full_name,
  role: state => state.user.role, // superuser, reviewer, tester
  permission_routes: state => state.permission.routes
}
export default getters
