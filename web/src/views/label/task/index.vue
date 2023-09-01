<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">标注任务管理</template>
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners"
      @syncAg="syncAg"
      @importSamples="importSamples"
      @getSamples="getSamples"
      @publishDataset="publishDataset"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
          <importExcel ref="import" :api="importSampleUrl" :showUpdate="false" :upload="uploadOptions" v-show="false"
            :successHandler="importSuccessHandler">导入</importExcel>
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
    <el-drawer
      title="样本列表"
      :visible.sync="drawer"
      direction="rtl">
      <el-table :data="samples" :show-header="false ">
        <el-table-column>
          <template slot-scope="scope">
            <el-descriptions size="mini" :column="3">
              <el-descriptions-item label="领域"><el-tag>{{ scope.row.domain }}</el-tag></el-descriptions-item>
              <el-descriptions-item label="权能"><el-tag>{{ scope.row.power }}</el-tag></el-descriptions-item>
              <el-descriptions-item label="语言"><el-tag>{{ scope.row.lang }}</el-tag></el-descriptions-item>
              <el-descriptions-item label="提示词">
                <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}" placeholder="请输入内容" :disabled="true" v-model="scope.row.prompt"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="输入文本">
                <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}" placeholder="请输入内容" :disabled="true" v-model="scope.row.input"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="输出文本">
                <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}" placeholder="请输入内容" :disabled="true" v-model="scope.row.output"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="标注提示词">
                <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}" placeholder="请输入内容" :disabled="true" v-model="scope.row.new_prompt"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="标注输入文本">
                <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}" placeholder="请输入内容" :disabled="true" v-model="scope.row.new_input"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="标注输出文本">
                <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}" placeholder="请输入内容" :disabled="true" v-model="scope.row.new_output"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="来源"><el-tag>{{ scope.row.source }}</el-tag></el-descriptions-item>
          </el-descriptions>
          </template>
        </el-table-column>
      </el-table>
    </el-drawer>
  </d2-container>
</template>

<script>
import * as api from './api'
import * as sampleApi from '../sample/api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import util from '@/libs/util'
export default {
  name: 'task',
  inject: ['refreshView'],
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      samples: [],
      samplePage: 1,
      currentId: false,
      drawer: false,
      importSampleUrl: "/api/label/samples/",
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
    syncAg (row) {
      api.SyncAg(row.row.id)
      this.doRefresh()
    },
    importSamples (row) {
      this.uploadOptions.open = true
      this.uploadOptions.url = util.baseURL() + `api/label/tasks/${row.row.id}/import_samples/`
    },
    importSuccessHandler(response, file, fileList) {
      console.log('上传成功')
      const that = this
      // that.upload.open = false
      that.uploadOptions.isUploading = false
      that.$refs.import.loading = true
      that.$refs.import.$refs.upload.clearFiles()
      // 是否更新已经存在的用户数据
      if (response.code === 2000) {
        that.$refs.import.loading = true
        that.$alert('导入成功', '导入完成', {
          confirmButtonText: '确定',
          callback: action => {
            that.refreshView()
          }
        })
      } else {
        that.$refs.import.loading = true
        that.$alert(response.msg, '导入失败', {
          confirmButtonText: '确定',
          callback: action => {
            that.refreshView()
          }
        })
      }
    },
    getSamples (row) {
      this.drawer = true
      sampleApi.GetList({task: row.row.id}, 10, this.samplePage).then((response) => {
        this.samples = response.data.data
      })
    },
    publishDataset (row) {
      pass
    }
  }
}
</script>
