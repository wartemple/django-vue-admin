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
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        width: 90,
        align: 'center',
        form: {
          disabled: true
        }
      },
      {
        title: '数据集名称',
        key: 'name',
        align: 'center',
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
            placeholder: '请输入数据集名称'
          }
        }
      },
      {
        title: '数据量',
        key: 'result_count',
        minWidth: 100,
        type: 'tag',
        align: 'center',
        form: {
          disabled: true
        }
      }
    ],
    rowHandle: {
      width: 290,
      view: {
        thin: true,
        text: ''
      },
      edit: {
        thin: true,
        text: ''
      },
      remove: {
        thin: true,
        text: ''
      },
      custom: [
        {
          thin: true,
          text: '',
          size: 'mini',
          type: 'primary',
          icon: 'el-icon-s-unfold',
          emit: 'downloadResult'
        },
        {
          thin: true,
          text: '导入标注结果',
          size: 'mini',
          type: 'primary',
          icon: 'el-icon-s-unfold',
          emit: 'importResults',
        },
      ]
    }
  }
}
