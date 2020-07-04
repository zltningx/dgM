<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="资产、域名、ip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select  v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
    </div>

    <el-table :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%" @sort-change="sortChange">
      <el-table-column sortable="custom" prop="id" align="center" label="ID" width="80" :class-name="getSortClass('id')">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column v-if="status === null" :show-overflow-tooltip="true" min-width="150px" label="资产名称">
        <template slot-scope="{row}">
          <!-- <router-link :to="'/vuls/workflow/'+row.id" class="link-type"> -->
            <span>{{ row.name }}</span>
          <!-- </router-link> -->
        </template>
      </el-table-column>

      <el-table-column :show-overflow-tooltip="true" min-width="150px" label="域名">
        <template slot-scope="{row}">
          <span>{{ row.domain }}</span>
        </template>
      </el-table-column>

      <el-table-column :show-overflow-tooltip="true" min-width="120px"  label="ip地址">
        <template slot-scope="scope">
          <span>{{ scope.row.ip }}</span>
        </template>
      </el-table-column>

      <el-table-column sortable="custom" prop="create_time"  width="180px" align="center" label="创建时间" :class-name="getSortClass('create_time')">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span>{{ scope.row.create_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column sortable="custom" prop="update_time"  width="180px" align="center" label="更新时间" :class-name="getSortClass('update_time')">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span>{{ scope.row.update_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column v-if="checkPermission(['superuser'])" align="center" label="操作" width="120">
        <template slot-scope="scope">
          <router-link :to="'/asset/edit/'+scope.row.id">
            <el-button
            type="primary" 
            size="small" 
            icon="el-icon-edit"
            circle>
            </el-button>
          </router-link>
          <el-button 
            type="danger" 
            size="small" 
            icon="el-icon-delete" 
            @click="handleDelete(scope.$index, scope.row)"
            circle>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :size.sync="listQuery.size" @pagination="getList" />
  </div>
</template>

<script>
// import permission from '@/directive/permission/index.js'
import checkPermission from '@/utils/permission' 
import { getAssets, deleteAsset } from '@/api/universal'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination
import waves from '@/directive/waves'
import { MessageBox, Message } from 'element-ui'
import { relative } from 'path'

export default {
  name: 'AssetTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 10,
        ordering: '-create_time'
      },
      sortOptions: [{ label: 'ID升序', key: 'id' }, { label: 'ID降序', key: '-id' },
      { label: '创建时间升序', key: 'create_time' }, { label: '创建时间降序', key: '-create_time' },
      { label: '更新时间升序', key: 'update_time' }, { label: '更新时间降序', key: '-update_time' }],
    }
  },
  created() {
    this.getList()
  },
  props: {
    'status': {
      type: Number,
      default: null
    },
    'own': {
      type: Boolean,
      default: false
    }
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true
      getAssets(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count
        this.listLoading = false
      })
    },
    handleDelete (index, row) {
      MessageBox.confirm('确认要删除?删除后不可恢复！', '确认删除', {
        confirmButtonText: '是的',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteAsset(row.id).then(() => {
          MessageBox({
            message: '删除成功',
            type: 'info',
            duration: 2 * 1000
          })
          this.getList()
        })
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    getSortClass: function(key) {
      const ordering = this.listQuery.ordering
      return ordering === `${key}`
        ? 'ascending'
        : ordering === `-${key}`
          ? 'descending'
          : ''
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      } else if (prop === 'create_time') {
        this.sortByCT(order)
      } else if (prop === 'update_time') {
        this.sortByDL(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.ordering = 'id'
      } else {
        this.listQuery.ordering = '-id'
      }
      this.handleFilter()
    },
    sortByCT(order) {
      if (order === 'ascending') {
        this.listQuery.ordering = 'create_time'
      } else {
        this.listQuery.ordering = '-create_time'
      }
      this.handleFilter()
    },
    sortByDL(order) {
      if (order === 'ascending') {
        this.listQuery.ordering = 'update_time'
      } else {
        this.listQuery.ordering = '-update_time'
      }
      this.handleFilter()
    },
  }
}
</script>

<style scoped>
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
</style>
