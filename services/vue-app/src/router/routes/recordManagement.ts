import { RouteRecordRaw, RouterView } from 'vue-router'
import { h } from 'vue'
import Main from '~/views/record-management/Main.vue'
import Upload from '~/views/record-management/Upload.vue'
import Overview from '~/views/record-management/Overview.vue'

export const recordManagementRoutes: RouteRecordRaw[] = [
  {
    path: 'record',
    component: { render: () => h(RouterView) },
    children: [
      {
        path: '',
        name: 'record',
        component: Main
      },
      {
        path: 'upload/:recordTypeId',
        name: 'record-upload',
        component: Upload
      },
      {
        path: 'overview/:recordTypeId',
        name: 'record-overview',
        component: Overview
      }
    ]
  }
]
