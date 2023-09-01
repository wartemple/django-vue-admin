export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%'
    },
    viewOptions: {
      componentType: 'row'
    },
    rowHandle: {
      width: 550,
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: [
        {
          thin: true,
          text: '同步标注结果',
          size: 'mini',
          type: 'primary',
          icon: 'el-icon-s-unfold',
          emit: 'syncAg',
          disabled (index, row) {
            return !row.sample_sum > 0
          },
        },
        {
          thin: true,
          text: '导入样本',
          size: 'mini',
          type: 'primary',
          icon: 'el-icon-s-unfold',
          emit: 'importSamples',
          disabled (index, row) {
            return row.sample_sum > 0
          },
        },
        {
          thin: true,
          text: '查看样本',
          size: 'mini',
          type: 'warning',
          icon: 'el-icon-s-unfold',
          emit: 'getSamples',
          disabled (index, row) {
            return !row.sample_sum > 0
          },
        },
        {
          thin: true,
          text: '发布数据集',
          size: 'mini',
          type: 'primary',
          icon: 'el-icon-s-unfold',
          emit: 'publishDataset',
          disabled (index, row) {
            return !row.status
          },
        },
      ]
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: '编码',
        key: 'id',
        width: 90,
        align: "center",
        form: {
          disabled: true
        }
      },
      {
        title: '标注任务名称',
        key: 'name',
        align: "center",
        search: {
          disabled: false
        },
        minWidth: 100,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入任务名称'
          }
        }
      },
      {
        title: '样本数',
        key: 'sample_sum',
        width: 80,
        align: "center",
        form: {
          disabled: true
        }
      },
      {
        title: '完成进度',
        key: 'schedule',
        minWidth: 100,
        type: 'table-progress',
        form: {
          disabled: true
        }
      },
      {
        title: '创建人',
        key: 'creator_name',
        width: 120,
        align: "center",
        form: {
          disabled: true
        }
        
      },
      {
        title: '创建时间',
        key: 'create_datetime',
        align: "center",
        width: 150,
        form: {
          disabled: true
        }
      }
    ]
  }
}
