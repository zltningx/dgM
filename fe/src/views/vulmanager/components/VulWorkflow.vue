<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" class="form-container">
      <el-card shadow="hover">
        <el-alert
          v-if="postForm.status == 0"
          title="警告！该工单流程还未由进入修复流程。"
          type="warning"
          show-icon>
        </el-alert>
        <el-steps :active="postForm.status" finish-status="success" simple style="margin-top: 20px">
          <el-step title="创建" ></el-step>
          <el-step title="修复中" ></el-step>
          <el-step title="复测" ></el-step>
        </el-steps>
      </el-card>
      <el-card shadow="hover">
        <div slot="header" class="clearfix">
          <span>漏洞详情</span>
          <router-link v-if="checkPermission(['superuser', 'reviewer', 'tester'])" :to="'/vuls/edit/'+ this.$route.params.id" class="link-type">
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </router-link>
        </div>
        <div class="createPost-main-container">
        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 40px;" prop="title" >
              <MDinput readonly v-model="postForm.title" :maxlength="100" name="name" required>
                标题
              </MDinput>
            </el-form-item>
            <div class="postInfo-container">
              <el-row>
                <el-col :span="8">
                    <el-form-item label-width="73px" label="漏洞类型:" class="postInfo-container-item" prop="vul_type">
                      <el-select disabled v-model="postForm.vul_type" filterable default-first-option placeholder="Search Type"   >
                        <el-option v-for="item in vulTypes" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label-width="73px" label="关联资产:" class="postInfo-container-item" prop="asset">
                    <el-select disabled v-model="postForm.asset" filterable default-first-option placeholder="Search Asset" >
                      <el-option v-for="item in assetOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label-width="73px" label="漏洞等级:" class="postInfo-container-item" prop="rank">
                      <el-select disabled v-model="postForm.rank">
                        <el-option v-for="item in ranks" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label-width="73px" label="漏洞链接:" prop="url" style="margin-bottom: 40px;">
                    <el-input readonly v-model="postForm.url" :rows="1" type="textarea" class="article-textarea" placeholder="请填写漏洞URL" />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-col>
        </el-row>
        <el-alert
          :closable="false"
          title="漏洞详情"
          type="info"
          show-icon
        />
        <el-form-item prop="mydescription" >
          <markdown-viewer ref="markdownViewer" v-model="postForm.description"  height="500px" /> 
        </el-form-item>
        <el-form-item label-width="73px" label="修复方案:" prop="repair" style="margin-bottom: 40px">
          <el-input readonly v-model="postForm.repair" type="textarea" autosize placeholder="请详细填写方案" />
        </el-form-item>
        <el-form-item label-width="48px" label="来源:" prop="resource" style="margin-bottom: 40px">
          <el-select disabled v-model="postForm.resource">
            <el-option v-for="item in resources" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="postForm.status > 0 && postForm.status != 3" label-width="73px" label="操作留言:" prop="workflow_description" style="margin-bottom: 40px;">
          <el-input v-model="sub_workflow.workflow_description" :rows="1" type="textarea" class="article-textarea" />
        </el-form-item>
        <el-form-item v-if="postForm.status > 0 && postForm.status != 3" style="margin-bottom: 40px;">
          <el-button v-if="postForm.status === 1" type="primary" @click="onPass(postForm.status)">确认修复</el-button>
          <el-button v-if="postForm.status === 2 && checkPermission(['superuser', 'reviewer', 'tester'])" type="primary" @click="onPass(postForm.status)">复测通过</el-button>
          <el-button v-if="postForm.status === 2 && checkPermission(['superuser', 'reviewer', 'tester'])" type="danger" @click="onRefuse">验证未修复</el-button>
        </el-form-item>
      </div>
      </el-card>
      <el-card shadow="hover" header="操作日志">
        <el-table
          :key='tableKey'
          border fit highlight-current-row
          :data="postForm.sub_workflow"
          style="width: 90%; margin:0 auto;"
          max-height="300">
          <el-table-column
            fixed
            prop="update_time"
            label="操作日期">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span>{{ scope.row.update_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="transactor"
            label="经办人">
            <template slot-scope="scope">
              <span>{{ scope.row.transactor.full_name }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="action"
            label="操作">
          </el-table-column>
          <el-table-column
            prop="workflow_description"
            label="意见">
          </el-table-column>
        </el-table>
      </el-card>
    </el-form>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' 
import MDinput from '@/components/MDinput'
import MarkdownViewer from '@/components/MarkdownViewer'
import { getVulTypes, getAssets, getVulWorkflow, editVulWorkflow, createVulSubWorkflow, vulTodoNotifiy } from '../../../api/universal'
import { MessageBox } from 'element-ui'

const defaultForm = {
  status: 0,
  title: '',
  asset: '',
  vul_type: '',
  rank: '',
  url: '',
  description: '',
  repair: '',
  resource: '',
  sub_workflow: []
}

export default {
  name: 'VulWorkflow',
  components: { MDinput, MarkdownViewer },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tableKey: 0,
      postForm: Object.assign({}, defaultForm),
      newForm: {
        "title": "",
        "asset": null,
        "vulnerability": {
          "status": 1,
          "vul_type": null,
          "rank": null,
          "url": "",
          "description": "",
          "repair": "",
        },
        "resource": null
      },
      sub_workflow: {vul_workflow: this.$route.params.id, action: '修复完成', workflow_description: ''},
      loading: false,
      userListOptions: [],
      assetOptions: [],
      vulTypes: [],
      ranks: [{
        label: '高危',
        value: 'H'
      }, {
        label: '中危',
        value: 'M'
      }, {
        label: '低危',
        value: 'L'
      }],
      resources: [{
        label: '外部SRC平台',
        value: 'external' 
      }, {
        label: '内部渗透测试',
        value: 'internal'
      }],
      tempRoute: {}
    }
  },
  computed: {
    // contentShortLength() {
    //   return this.postForm.content_short.length
    // },
    // displayTime: {
    //   // set and get is useful when the data
    //   // returned by the back end api is different from the front end
    //   // back end return => "2013-06-25 06:59:25"
    //   // front end need timestamp => 1372114765000
    //   get() {
    //     return (+new Date(this.postForm.dead_line))
    //   },
    //   set(val) {
    //     this.postForm.dead_line = new Date(val)
    //   }
    // },
    displayUpdateTime: {
      // set and get is useful when the data
      // returned by the back end api is different from the front end
      // back end return => "2013-06-25 06:59:25"
      // front end need timestamp => 1372114765000
      get() {
        return (+new Date(this.postForm.sub_workflow.update_time))
      },
      set(val) {
        this.postForm.sub_workflow.update_time = new Date(val)
      }
    }
  },
  created() {
    this.fetchVulTypes()
    this.fetchAssets()
    const id = this.$route.params && this.$route.params.id
    this.fetchData(id)
    // Why need to make a copy of this.$route here?
    // Because if you enter this page and quickly switch tag, may be in the execution of the setTagsViewTitle function, this.$route is no longer pointing to the current page
    // https://github.com/PanJiaChen/vue-element-admin/issues/1221
    this.tempRoute = Object.assign({}, this.$route)  
  },
  methods: {
    checkPermission,
    fetchVulTypes() {
      getVulTypes().then(response => {
        if (!response.data) return
        this.vulTypes = response.data.map((type) => {
          var newType = {};
          newType['label'] = type[1];
          newType['value'] = type[0];
          return newType;
        })
      })
    },
    fetchAssets() {
      getAssets().then(response => {
        this.assetOptions = response.results.map((asset) => {
          var newAsset = {};
          newAsset['label'] = asset.name + ' - ' + asset.domain;
          newAsset['value'] = asset.id;
          return newAsset;
        })
      })
    },
    fetchData(id) {
      getVulWorkflow(id).then(response => {
        this.postForm.title = response.title
        this.postForm.asset = response.asset
        this.postForm.resource = response.resource
        this.postForm.sub_workflow = response.sub_workflow
        this.postForm.status = response.vulnerability.status
        this.postForm.vul_type = response.vulnerability.vul_type
        this.postForm.rank = response.vulnerability.rank 
        this.postForm.url = response.vulnerability.url
        this.postForm.description = response.vulnerability.description
        this.postForm.repair = response.vulnerability.repair
        // set tagsview title
        // this.setTagsViewTitle()
        
        // set page title
        this.setPageTitle()
      })
    },
    setTagsViewTitle() {
      // const title = 'Ticket Workflow'
      // const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      // this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    setPageTitle() {
      const title = 'Ticket Workflow'
      // document.title = `${title} - ${this.postForm.id}`
    },
    setNewForm() {
      this.newForm.title = this.postForm.title
      this.newForm.asset = this.postForm.asset
      this.newForm.resource = this.postForm.resource
      this.newForm.vulnerability.status = this.postForm.status
      this.newForm.vulnerability.vul_type = this.postForm.vul_type
      this.newForm.vulnerability.rank = this.postForm.rank
      this.newForm.vulnerability.url = this.postForm.url
      this.newForm.vulnerability.description = this.postForm.description
      this.newForm.vulnerability.repair = this.postForm.repair
    },
    onPass() {
      this.loading = false
      this.postForm.status += 1
      const id = this.$route.params.id
      this.setNewForm()
      editVulWorkflow(id, this.newForm).then(res => {
        if (this.postForm.status == 2) {
          this.sub_workflow.action = '修复漏洞完成'
          let params = {id: res.id, message: ''}
          vulTodoNotifiy(params).then().catch()
        } else if (this.postForm.status == 3) {
          this.sub_workflow.action = '复测通过'
        }
        if (this.sub_workflow.workflow_description === ''){
          this.sub_workflow.workflow_description = "无"
        }
        createVulSubWorkflow(this.sub_workflow).then(res => {
          this.fetchData(this.$route.params.id)
          this.$notify({
            title: '成功',
            message: '处理成功',
            type: 'success',
            duration: 2 * 1000
          })
          this.loading = false
        }).catch()
      })
      this.loading = false
    },
    onRefuse() {
      if (this.sub_workflow.workflow_description != '') {
        this.loading = true
        this.postForm.status = 1
        const id = this.$route.params.id
        this.setNewForm()
        editVulWorkflow(id, this.newForm).then(res => {
          this.sub_workflow.action = '复测不通过'
          let params = {id: res.id, message: '您的漏洞经过复测未通过测试'}
          vulTodoNotifiy(params).then().catch()
          createVulSubWorkflow(this.sub_workflow).then(res => {
            this.fetchData(this.$route.params.id)
            this.loading = false
            this.$notify({
              title: '拒绝',
              message: '复测不通过，打回修复',
              type: 'warning',
              duration: 2 * 1000
            })
          })
        })
      } else {
        this.$message({
            message: 'Submit Form Error | 复测不通过时，操作留言为必填',
            type: 'error',
            duration: 2000
          })
        this.loading = false
        return false
      }
    },
  }
}
</script>

<style lang="scss" scoped>
@import "~@/styles/mixin.scss";

.createPost-container {
  position: relative;

  .createPost-main-container {
    padding: 40px 45px 20px 50px;

    .postInfo-container {
      position: relative;
      @include clearfix;
      margin-bottom: 10px;

      .postInfo-container-item {
        float: left;
      }
    }
  }

  .word-counter {
    width: 40px;
    position: absolute;
    right: 10px;
    top: 0px;
  }
}

.article-textarea /deep/ {
  textarea {
    padding-right: 40px;
    resize: none;
    border: none;
    border-radius: 0px;
    border-bottom: 1px solid #bfcbd9;
  }
}
.editor-container{
  margin-bottom: 30px;
}
</style>
