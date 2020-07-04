<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="标题、Url" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-if="status === null" v-model="listQuery.vulnerability__status" placeholder="Stauts" clearable style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in statusOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-if="status === null" v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-else v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortCreateOptions" :key="item.key" :label="item.label" :value="item.key" />
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

      <el-table-column v-if="status === null" :show-overflow-tooltip="true" min-width="150px" label="标题">
        <template slot-scope="{row}">
          <router-link :to="'/vuls/workflow/'+row.id" class="link-type">
            <span>{{ row.title }}</span>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column :show-overflow-tooltip="true" min-width="150px" label="漏洞链接">
        <template slot-scope="{row}">
          <span v-if="status !== null">{{ row.url }}</span>
          <span v-else>{{ row.vulnerability.url }}</span>
        </template>
      </el-table-column>

      <el-table-column  width="120px" align="center" label="报告人">
        <template slot-scope="scope">
          <span v-if="status === null">{{ scope.row.vulnerability.reporter.full_name }}</span>
          <span v-else >{{ scope.row.reporter.full_name }}</span>
        </template>
      </el-table-column>

      <el-table-column  width="180px" align="center" label="漏洞类型">
        <template slot-scope="scope">
          <span v-if="status !== null">{{ vulTypes[scope.row.vul_type] }}</span>
          <span v-else>{{ vulTypes[scope.row.vulnerability.vul_type] }}</span>
        </template>
      </el-table-column>

      <el-table-column class-name="status-col" label="等级" width="100">
        <template slot-scope="{row}">
          <el-tag v-if="status !== null" :type="row.rank | rankFilter('type')">
            {{ row.rank | rankFilter('name') }}
          </el-tag>
          <el-tag v-else :type="row.vulnerability.rank | rankFilter('type')">
            {{ row.vulnerability.rank | rankFilter('name') }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column sortable="custom" prop="create_time"  width="180px" align="center" label="创建时间" :class-name="getSortClass('create_time')">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span v-if="status !== null">{{ scope.row.create_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
          <span v-else>{{ scope.row.vulnerability.create_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column class-name="status-col" label="Status" width="100">
        <template slot-scope="{row}">
          <el-tag v-if="status !== null" :type="row.status | statusFilter('type')">
            {{ row.status | statusFilter('name') }}
          </el-tag>
          <el-tag v-else :type="row.vulnerability.status | statusFilter('type')">
            {{ row.vulnerability.status | statusFilter('name') }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column v-if="checkPermission(['superuser', 'reviewer', 'tester'])" align="center" label="操作" width="120">
        <template slot-scope="scope">
          <router-link v-if="status===null" :to="'/vuls/edit/'+scope.row.id">
            <el-button
            type="primary" 
            size="small" 
            icon="el-icon-edit"
            circle>
            </el-button>
          </router-link>
          <router-link v-else :to="'/vuls/complete/'+scope.row.id">
            <el-button
            type="primary" 
            size="small" 
            icon="el-icon-edit-outline"
            circle>
            </el-button>
          </router-link>
          <el-button 
          v-if="checkPermission(['superuser'])"
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
import { getVuls, getVulWorkflows, getVulTypes, deleteVulWorkflow, deleteVul } from '@/api/universal'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination
import waves from '@/directive/waves'
import { MessageBox, Message } from 'element-ui'
import { relative } from 'path'

export default {
  name: 'VulTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status, type) {
      const statusMap = {
        'type': {
          0: 'primary',
          1: 'danger',
          2: 'warning',
          3: 'success',
        },
        'name': {
          0: '创建',
          1: '修复中',
          2: '复测中',
          3: '已修复',
        }
      }
      return statusMap[type][status]
    },
    rankFilter(rank, type) {
      const rankMap = {
        'type': {
          'H': 'danger',
          'M': 'warning',
          "L": 'primary',
        },
        'name': {
          'H': '高危',
          'M': '中危',
          "L": '低危',
        }
      }
      return rankMap[type][rank]
    },
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      vulTypes: {},
      listQuery: {
        page: 1,
        size: 10,
        ordering: '-vulnerability__create_time'
      },
      showReviewer: false,
      statusOptions: [{ label: '修复中', key: 1 }, { label: '复测中', key: 2 }, { label: '已修复', key: 3 }],
      sortCreateOptions: [{ label: 'ID升序', key: 'id' }, { label: 'ID降序', key: '-id' },
      { label: '创建时间升序', key: 'create_time' }, { label: '创建时间降序', key: '-create_time' }],
      sortOptions: [{ label: 'ID升序', key: 'id' }, { label: 'ID降序', key: '-id' },
      { label: '创建时间升序', key: 'vulnerability__create_time' }, { label: '创建时间降序', key: '-vulnerability__create_time' }],
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
      if (this.status !== null) {
        this.listQuery.status = this.status
        this.listQuery.ordering = '-create_time'
      }
      if (this.own) {
        this.listQuery.type = 'own'
      }
      getVulTypes().then(response => {
        if (!response.data) return
        for (let i = 0; i < response.data.length; i++){
          this.vulTypes[response.data[i][0]] = response.data[i][1]
        }
        if (this.status !== null) {
          getVuls(this.listQuery).then(response => {
            this.list = response.results
            this.total = response.count
            this.listLoading = false
          })
        } else {
          getVulWorkflows(this.listQuery).then(response => {
            this.list = response.results
            this.total = response.count
            this.listLoading = false
          })
        }
      })
    },
    handleDelete (index, row) {
      MessageBox.confirm('确认要删除?删除后不可恢复！', '确认删除', {
        confirmButtonText: '是的',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (this.status === null) {
          deleteVulWorkflow(row.id).then(() => {
            MessageBox({
              message: '删除成功',
              type: 'info',
              duration: 2 * 1000
            })
            this.getList()
          })
        } else {
          deleteVul(row.id).then(() => {
            MessageBox({
              message: '删除成功',
              type: 'info',
              duration: 2 * 1000
            })
            this.getList()
          })
        }
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
      } else if (prop === 'dead_line') {
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
