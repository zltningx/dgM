<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="主题、申请人、业务线" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.status" placeholder="Stauts" clearable style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in statusOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        优先级
      </el-checkbox>
    </div>

    <el-table :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%" @sort-change="sortChange">
      <el-table-column sortable="custom" prop="id" align="center" label="ID" width="80" :class-name="getSortClass('id')">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column :show-overflow-tooltip="true" min-width="300px" label="主题">
        <template slot-scope="{row}">
          <!-- <router-link v-if="checkPermission(['superuser']) || show === 'own'" :to="'/tickets/edit/'+row.id" class="link-type">
            <span>{{ row.title }}</span>
          </router-link> -->
          <router-link :to="'/tickets/workflow/'+row.id" class="link-type">
            <span>{{ row.title }}</span>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column sortable="custom" prop="dead_line" width="180px" align="center" label="最迟交付日期" :class-name="getSortClass('dead_line')">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span>{{ scope.row.dead_line | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column width="120px" align="center" label="申请人">
        <template slot-scope="scope">
          <span v-if="scope.row.creator.full_name === ''">{{ scope.row.creator.username }}</span>
          <span v-else>{{ scope.row.creator.full_name }}</span>
        </template>
      </el-table-column>

      <el-table-column v-if="showReviewer" label="优先级" width="110px" align="center">
        <template slot-scope="scope">
          <svg-icon v-for="n in +scope.row.priority" :key="n" icon-class="star" class="meta-item__icon" />
        </template>
      </el-table-column>

      <el-table-column  width="120px" align="center" label="业务线(部门)">
        <template slot-scope="scope">
          <span>{{ scope.row.department }}</span>
        </template>
      </el-table-column>

      <el-table-column sortable="custom" prop="create_time"  width="180px" align="center" label="创建时间" :class-name="getSortClass('create_time')">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span>{{ scope.row.create_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column class-name="status-col" label="Status" width="110">
        <template slot-scope="{row}">
          <el-tag :type="row.status | statusFilter('type')">
            {{ row.status | statusFilter('name') }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column v-if="checkPermission(['superuser']) || this.show === 'own'" align="center" label="操作" width="120">
        <template slot-scope="scope">
          <router-link :to="'/tickets/edit/'+scope.row.id">
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
import { getTickets, deleteTicket } from '@/api/universal'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination
import waves from '@/directive/waves'
import { MessageBox, Message } from 'element-ui'
import { relative } from 'path'

export default {
  name: 'TicketTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status, type) {
      const statusMap = {
        'type': {
          0: 'warning',
          1: 'primary',
          2: 'danger',
          3: 'success',
        },
        'name': {
          0: '草稿',
          1: '审核&分配',
          2: '测试中',
          3: '测试完成',
        }
      }
      return statusMap[type][status]
    },

  },
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
      showReviewer: false,
      statusOptions: [{ label: '等待测试', key: 0 }, { label: '审核&分配', key: 1 },
      { label: '测试中', key: 2 }, { label: '测试完成', key: 3 }],
      sortOptions: [{ label: 'ID升序', key: 'id' }, { label: 'ID降序', key: '-id' },
      { label: '创建时间升序', key: 'create_time' }, { label: '创建时间降序', key: '-create_time' },
      { label: '最后日期升序', key: 'dead_line' }, { label: '最后日期降序', key: '-dead_line' }],
    }
  },
  created() {
    this.getList()
  },
  props: {
    'show': {
      type: String,
      default: 'relative'
    }
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true
      if (this.show === 'own') {
        this.listQuery.type = 'own'
      } else if (this.show == 'todo') {
        this.listQuery.type = 'todo'
      }
      getTickets(this.listQuery).then(response => {
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
        deleteTicket(row.id).then(() => {
          MessageBox({
            message: '删除成功',
            type: 'info',
            duration: 2 * 1000
          })
          this.getList()
        }).catch()
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
    sortByDL(order) {
      if (order === 'ascending') {
        this.listQuery.ordering = 'dead_line'
      } else {
        this.listQuery.ordering = '-dead_line'
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
