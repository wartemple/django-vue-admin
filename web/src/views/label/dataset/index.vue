<template>
  <d2-container  :class="{'page-compact':crud.pageOptions.compact}">
    <template slot="header">数据集管理</template>
    <d2-crud-x
        ref="d2Crud"
        v-bind="_crudProps"
        v-on="_crudListeners"
        @importResults="importResults"
        @downloadResult="downloadResult"
    >
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch"  />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
          <importExcel ref="import" :api="importSampleUrl" :showUpdate="false" :upload="uploadOptions" v-show="false"
            :successHandler="importSuccessHandler">导入</importExcel>
        </el-button-group>
      </div>
    </d2-crud-x>

  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import util from '@/libs/util'

export default {
  name: 'Dataset',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      importSampleUrl: '/api/label/label_results/',
      uploadOptions: {
        open: false,
        title: '',
        isUploading: false,
        updateSupport: 0,
        headers: { Authorization: 'JWT ' + util.cookies.get('token') },
        url: util.baseURL() + 'api/label/file/'
      }
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    },
    addRequest (row) {
      console.log('api', api)
      return api.AddObj(row)
    },
    updateRequest (row) {
      console.log('----', row)
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    downloadResult (row) {
      return api.exportData({ dataset: row.row.id })
    },
    importResults (row) {
      this.uploadOptions.open = true
      this.uploadOptions.url = util.baseURL() + `api/label/datasets/${row.row.id}/import_results/`
    },
    importSuccessHandler (response, file, fileList) {
      const that = this
      // that.upload.open = false
      that.uploadOptions.isUploading = false
      that.$refs.import.loading = true
      that.$refs.import.$refs.upload.clearFiles()
      // 是否更新已经存在的用户数据
      if (response.code === 2000) {
        that.$refs.import.loading = false
        that.$alert('导入成功', '导入完成', {
          confirmButtonText: '确定',
          callback: action => {
            this.uploadOptions.open = false
            this.doRefresh()
          }
        })
      } else {
        that.$refs.import.loading = false
        that.$alert(response.msg, '导入失败', {
          confirmButtonText: '确定',
          callback: action => {
            this.uploadOptions.open = false
            this.doRefresh()
          }
        })
      }
    }
  }
}
</script>
