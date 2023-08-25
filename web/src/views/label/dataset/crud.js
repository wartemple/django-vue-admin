import { request } from '@/api/service'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    searchOptions: {
      show: true
    },
    options: {
      height: '100%'
    },
    viewOptions: {
      componentType: 'row'
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: '查看',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '修改',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '删除',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: '编码',
        key: 'id',
        width: 90,
        form: {
          disabled: true
        }
      },
      {
        title: '数据集名称',
        key: 'name',
        sortable: true,
        minWidth: 100,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入数据集名称'
          }
        }
      },
      {
        title: '创建人',
        key: 'creator',
        width: 120,
        form: {
          disabled: true
        }
      },
      {
        title: '创建时间',
        key: 'create_datetime',
        width: 150,
        form: {
          disabled: true
        }
      },
    ]
  }
}
