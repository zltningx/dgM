import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: '首页', icon: 'dashboard', affix: true }
      }
    ]
  }
]

export const asyncRoutes = [
  {
    path: '/tickets',
    component: Layout,
    redirect: '/tickets/todo',
    name: 'Tickets',
    meta: {
      title: '安全测试工单',
      icon: 'example'
    },
    children: [
      {
        path: 'create',
        component: () => import('@/views/tickets/create'),
        name: 'CreateTicket',
        meta: { title: '新建工单', icon: 'edit' }
      },
      {
        path: 'todo',
        component: () => import('@/views/tickets/list_todo'),
        name: 'TicketsListTodo',
        meta: { title: '我的待办', icon: 'list' }
      },
      {
        path: 'edit/:id(\\d+)',
        component: () => import('@/views/tickets/edit'),
        name: 'EditTickets',
        meta: { title: '编辑工单', noCache: true, activeMenu: '/tickets/edit' },
        hidden: true
      },
      {
        path: 'workflow/:id(\\d+)',
        component: () => import('@/views/tickets/workflow'),
        name: 'workflow',
        meta: { title: '工作流', noCache: true, activeMenu: '/tickets/workflow' },
        hidden: true
      },
      {
        path: 'own',
        component: () => import('@/views/tickets/list_own'),
        name: 'TicketsListOwn',
        meta: { title: '我的工单', icon: 'list' }
      },
      {
        path: 'all',
        component: () => import('@/views/tickets/list_all'),
        name: 'TicketsListAll',
        meta: { title: '所有工单', icon: 'list', roles: ['superuser', 'reviewer'] }
      }
    ]
  },
  {
    path: '/vuls',
    component: Layout,
    redirect: '/vuls/unactive',
    name: 'Vuls',
    meta: {
      title: '漏洞管理',
      icon: 'table'
    },
    children: [
      {
        path: 'unactive',
        component: () => import('@/views/vulmanager/list_create'),
        name: 'VulListCreate',
        meta: { title: '待完善漏洞', icon: 'list' }
      },
      {
        path: 'create',
        component: () => import('@/views/vulmanager/create'),
        name: 'CreateVulWorkflow',
        meta: { title: '创建漏洞流', icon: 'edit', roles: ['superuser', 'reviewer', 'tester'] }
      },
      {
        path: 'edit/:id(\\d+)',
        component: () => import('@/views/vulmanager/edit'),
        name: 'EditVulWorkflow',
        meta: { title: '编辑漏洞流', noCache: true, activeMenu: '/vuls/edit', roles: ['superuser', 'reviewer', 'tester'] },
        hidden: true
      },
      {
        path: 'complete/:id(\\d+)',
        component: () => import('@/views/vulmanager/complete'),
        name: 'CompleteVulWorkflow',
        meta: { title: '完善漏洞流', noCache: true, activeMenu: '/vuls/complete', roles: ['superuser', 'reviewer', 'tester'] },
        hidden: true
      },
      {
        path: 'own',
        component: () => import('@/views/vulmanager/list_own'),
        name: 'VulListOwn',
        meta: { title: '我报告的漏洞', icon: 'list', roles: ['superuser', 'reviewer', 'tester'] }
      },
      {
        path: 'all',
        component: () => import('@/views/vulmanager/list_all'),
        name: 'VulListAll',
        meta: { title: '所有漏洞流', icon: 'list' }
      },
      {
        path: 'workflow/:id(\\d+)',
        component: () => import('@/views/vulmanager/workflow'),
        name: 'Workflow',
        meta: { title: '漏洞修复流', noCache: true, activeMenu: '/vuls/workflow' },
        hidden: true
      }
    ]
  },
  {
    path: '/asset',
    component: Layout,
    name: 'Asset',
    meta: { title: '资产管理', icon: 'chart', roles: ['superuser'] },
    children: [
      {
        path: 'create',
        component: () => import('@/views/asset/create'),
        name: 'CreateAsset',
        meta: { title: '登记新资产', icon: 'edit' }
      },
      {
        path: 'edit/:id(\\d+)',
        component: () => import('@/views/asset/edit'),
        name: 'EditAsset',
        meta: { title: '编辑资产', noCache: true, activeMenu: '/asset/edit' },
        hidden: true
      },
      {
        path: 'all',
        name: 'AssetsList',
        component: () => import('@/views/asset/list_all'),
        meta: { title: '资产列表', icon: 'list' }
      }
    ]
  },
  {
    path: '/settings',
    component: Layout,
    name: 'Settings',
    meta: { title: '配置', icon: 'nested', roles: ['superuser'] },
    children: [
      {
        path: 'smtp',
        name: 'SMTPConfig',
        component: () => import('@/views/settings/smtp'),
        meta: { title: 'SMTP配置', icon: 'form' }
      }
      // {
      //   path: 'other',
      //   name: 'Other',
      //   meta: { title: '其它配置', icon: 'form' }
      // }
    ]
  },
  // {
  //   path: '/nested',
  //   component: Layout,
  //   redirect: '/nested/menu1',
  //   name: 'Nested',
  //   meta: {
  //     title: 'Nested',
  //     icon: 'nested'
  //   },
  //   children: [
  //     {
  //       path: 'menu1',
  //       component: () => import('@/views/nested/menu1/index'), // Parent router-view
  //       name: 'Menu1',
  //       meta: { title: 'Menu1' },
  //       children: [
  //         {
  //           path: 'menu1-1',
  //           component: () => import('@/views/nested/menu1/menu1-1'),
  //           name: 'Menu1-1',
  //           meta: { title: 'Menu1-1' }
  //         },
  //         {
  //           path: 'menu1-2',
  //           component: () => import('@/views/nested/menu1/menu1-2'),
  //           name: 'Menu1-2',
  //           meta: { title: 'Menu1-2' },
  //           children: [
  //             {
  //               path: 'menu1-2-1',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
  //               name: 'Menu1-2-1',
  //               meta: { title: 'Menu1-2-1' }
  //             },
  //             {
  //               path: 'menu1-2-2',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
  //               name: 'Menu1-2-2',
  //               meta: { title: 'Menu1-2-2' }
  //             }
  //           ]
  //         },
  //         {
  //           path: 'menu1-3',
  //           component: () => import('@/views/nested/menu1/menu1-3'),
  //           name: 'Menu1-3',
  //           meta: { title: 'Menu1-3' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'menu2',
  //       component: () => import('@/views/nested/menu2/index'),
  //       meta: { title: 'menu2' }
  //     }
  //   ]
  // },
  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
        meta: { title: 'External Link', icon: 'link' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
