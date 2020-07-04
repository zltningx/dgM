<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">
      <el-card shadow="hover">
        <el-alert
          v-if="postForm.status == 0"
          title="警告！该工单流程还未由发起人发起。"
          type="warning"
          show-icon>
        </el-alert>
        <el-steps :active="postForm.status" finish-status="success" simple style="margin-top: 20px">
          <el-step title="发起流程" ></el-step>
          <el-step title="审核&分配" ></el-step>
          <el-step title="测试" ></el-step>
        </el-steps>
      </el-card>
      <el-card shadow="hover">
        <div slot="header" class="clearfix">
          <span>工单详情</span>
          <router-link v-if="checkPermission(['superuser']) || this.postForm.creator.username === this.$store.getters.name" :to="'/tickets/edit/'+ this.$route.params.id" class="link-type">
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </router-link>
        </div>
        <div class="createPost-main-container">
          <el-row>
            <el-col :span="24">
              <el-form-item style="margin-bottom: 40px;" prop="title">
                <MDinput v-model="postForm.title" :maxlength="100" name="name" :readonly="true" required>
                  主题
                </MDinput>
              </el-form-item>
              <el-form-item v-if="this.isEdit" label-width="58px" label="创建人:" class="postInfo-container-item" prop="creator" >
                <el-input v-model="postForm.creator.full_name" :rows="1" type="textarea" class="article-textarea" :readonly="true" style="width: 15%; margin-bottom: 20px;"/>
              </el-form-item>
              <div class="postInfo-container">
                <el-row>
                  <el-col :span="10">
                    <el-form-item v-if="postForm.status == 1" label-width="58px" label="经办人:" class="postInfo-container-item" prop="transactors">
                      <el-select v-model="postForm.transactors" multiple filterable default-first-option placeholder="Search user" style="width: 200%"  >
                        <el-option v-for="item in SecUserListOptions" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                    <el-form-item v-else-if="postForm.status > 1" label-width="58px" label="经办人:" class="postInfo-container-item" prop="transactors">
                      <el-select v-model="postForm.transactors" disabled multiple filterable placeholder="Search user" style="width: 100%"  >
                        <el-option v-for="item in SecUserListOptions" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                    <el-form-item v-else label-width="58px" label="经办人:" class="postInfo-container-item" prop="transactors">
                      <el-select v-model="postForm.transactors" disabled multiple filterable placeholder="Search user" style="width: 100%"  >
                        <el-option v-for="item in userListOptions" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                  </el-col>

                  <el-col :span="9">
                    <el-form-item label-width="120px" label="期望完成日期:" class="postInfo-container-item" prop="dead_line">
                      <el-date-picker v-model="displayTime" type="datetime" format="yyyy-MM-dd HH:mm:ss" :readonly="true" placeholder="Select date and time" />
                    </el-form-item>
                  </el-col>

                  <el-col :span="5">
                    <el-form-item label-width="90px"  label="优先级:" class="postInfo-container-item" prop="priority">
                      <el-rate
                        disabled
                        v-model="postForm.priority"
                        :max="3"
                        :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                        :low-threshold="1"
                        :high-threshold="3"
                        style="display:inline-block"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
            </el-col>
          </el-row>

          <el-form-item  label-width="95px" label="业务线(部门):" prop="department" style="margin-bottom: 40px;">
            <el-input v-model="postForm.department" :rows="1" type="textarea" class="article-textarea" placeholder="请填写全名" :readonly="true" />
          </el-form-item>

          <el-card shadow="hover" header="需求详情" style="margin-bottom: 40px;">
            <el-form-item prop="description" >
              <markdown-viewer ref="markdownViewer" v-model="postForm.description"  height="500px" /> 
            </el-form-item>
          </el-card>
          <div v-if="postForm.status === 2">
            <el-form-item label-width="100px" label="测试结果描述:" prop="result_description" style="margin-bottom: 40px;">
              <el-input v-model="ticket_result.result_description" :rows="1" autosize type="textarea" placeholder="请总结测试的结果"  />
            </el-form-item>
            <el-card v-for="vul in ticket_result.vulnerabilities" :key="vul.key" shadow="hover" style="margin-bottom: 10px;"  >
              <div slot="header" class="clearfix">
                <span>漏洞信息</span>
                  <el-button style="float: right;  padding: 3px 3px" type="danger" @click="removeVul(vul)" circle icon="el-icon-delete"></el-button>
              </div>
              <el-form-item label-width="73px" label="漏洞地址:" prop="url" style="margin-bottom: 40px;">
                <el-input v-model="vul.url" :rows="1" type="textarea" class="article-textarea" />
              </el-form-item>
              <el-row>
                <el-col :span="7">
                    <el-form-item label-width="73px" label="漏洞类型:" class="postInfo-container-item" prop="vul_type">
                      <el-select v-model="vul.vul_type" filterable default-first-option placeholder="Search Type"   >
                        <el-option v-for="item in vulTypes" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="7">
                    <el-form-item label-width="73px" label="漏洞等级:" class="postInfo-container-item" prop="rank">
                      <el-select v-model="vul.rank">
                        <el-option v-for="item in ranks" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
              </el-row>
              <el-form-item style="margin-bottom: 10px;" prop="description" >
                <markdown-editor ref="markdownEditor" v-model="vul.description" :language="'zh_CN'" height="500px" /> 
              </el-form-item>
              <el-form-item label-width="73px" label="修复方案:" prop="repair" style="margin-bottom: 40px; width: 50%">
                <el-input v-model="vul.repair" :rows="1" type="textarea" autosize placeholder="请详细填写方案" />
              </el-form-item>
            </el-card>
            <el-button type="info" size="mini" icon="el-icon-plus" @click="addVul" style="margin-bottom: 20px;">新增漏洞</el-button>
          </div>
          <div v-if="postForm.status === 3">
            <el-form-item label-width="100px" label="测试结果描述:" prop="result_description" style="margin-bottom: 40px;">
              <el-input v-model="ticket_result.result_description" :rows="1" autosize type="textarea" placeholder="请总结测试的结果" readonly />
            </el-form-item>
            <el-card v-for="vul in ticket_result.vulnerabilities" :key="vul.key" shadow="hover" style="margin-bottom: 10px;"  >
              <div slot="header" class="clearfix">
                <span>漏洞信息</span>
              </div>
              <el-form-item label-width="73px" label="漏洞地址:" prop="url" style="margin-bottom: 40px;">
                <el-input v-model="vul.url" :rows="1" type="textarea" class="article-textarea" readonly />
              </el-form-item>
              <el-row>
                <el-col :span="7">
                    <el-form-item label-width="73px" label="漏洞类型:" class="postInfo-container-item" prop="vul_type">
                      <el-select v-model="vul.vul_type" disabled filterable default-first-option placeholder="Search Type"   >
                        <el-option v-for="item in vulTypes" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="7">
                    <el-form-item label-width="73px" label="漏洞等级:" class="postInfo-container-item" prop="rank">
                      <el-select v-model="vul.rank" disabled >
                        <el-option v-for="item in ranks" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
              </el-row>
              <el-card shadow="hover" header="漏洞详情" style="margin-bottom: 40px;">
                <el-form-item prop="vul_description" >
                  <markdown-viewer ref="vul_markdownViewer" v-model="vul.description" height="500px" /> 
                </el-form-item>
              </el-card>
              <el-form-item label-width="73px" label="修复方案:" prop="repair" style="margin-bottom: 40px; width: 50%">
                <el-input v-model="vul.repair" :rows="1" type="textarea" autosize placeholder="请详细填写方案" readonly />
              </el-form-item>
            </el-card>
          </div>
          <el-form-item v-if="postForm.status > 0 && postForm.status != 3 && this.$store.getters.role != 'user'" label-width="73px" label="审批意见:" prop="workflow_description" style="margin-bottom: 40px;">
            <el-input v-model="sub_workflow.workflow_description" :rows="1" type="textarea" class="article-textarea" />
          </el-form-item>

           <el-form-item v-if="postForm.status > 0 && postForm.status != 3 && this.$store.getters.role != 'user'" style="margin-bottom: 40px;">
              <el-button v-if="postForm.status < 3" type="primary" @click="onPass">通过</el-button>
              <el-button v-if="postForm.status == 1" type="danger" @click="onRefuse">拒绝</el-button>
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
import MarkdownEditor from '@/components/MarkdownEditor'
import { validURL } from '@/utils/validate'
import { getTicket, newTicket, editTicket, createSubWorkflow, getVulTypes, createTicketResult, penTodoNotifiy } from '../../../api/universal'
import { getTransactors, getSecGroup } from '../../../api/user'
import { MessageBox } from 'element-ui'

const defaultForm = {
  status: 0,
  title: '',
  creator: '',
  priority: 1, // 优先级
  department: '',
  dead_line: '',
  description: '',
  transactors: [],
  sub_workflow: null,
}

export default {
  name: 'TicketWorkflow',
  components: { MDinput, MarkdownViewer, MarkdownEditor },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    const validateRequire = (rule, value, callback) => {
      if (value === '' || value === [] || value === undefined) {
        this.$message({
          message: rule.field + '是必填项',
          type: 'error'
        })
        callback(new Error(rule.field + '是必填项'))
      } else {
        callback()
      }
    }
    return {
      tableKey: 0,
      postForm: Object.assign({}, defaultForm),
      sub_workflow: {penetration_test_ticket: this.$route.params.id, action: '同意', workflow_description: ''},
      ticket_result: {
        vulnerabilities: [{
          url: '',
          vul_type: '',
          rank: '',
          description: '## 请详细填写漏洞详情',
          repair: ''
        }],
        result_description: "",
        penetration_test_ticket: this.$route.params.id},
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
      status: {0: 'draft', 1: 'publish'},
      loading: false,
      userListOptions: [],
      secUserListOptions: [],
      oldTransactors: [],
      rules: {
        title: [{ validator: validateRequire, trigger: 'blur' }],
        description: [{ validator: validateRequire, trigger: 'blur' }],
        dead_line: [{ validator: validateRequire, trigger: 'blur' }],
        transactors: [{ validator: validateRequire, trigger: 'blur'}],
        department: [{ validator: validateRequire, trigger: 'blur' }],
        priority: [{ validator: validateRequire, trigger: 'blur' }],
      },
      tempRoute: {}
    }
  },
  computed: {
    // contentShortLength() {
    //   return this.postForm.content_short.length
    // },
    displayTime: {
      // set and get is useful when the data
      // returned by the back end api is different from the front end
      // back end return => "2013-06-25 06:59:25"
      // front end need timestamp => 1372114765000
      get() {
        return (+new Date(this.postForm.dead_line))
      },
      set(val) {
        this.postForm.dead_line = new Date(val)
      }
    },
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
    this.fetchTranUser()
    this.fetchVulTypes()
    if (this.isEdit) {
      const id = this.$route.params && this.$route.params.id
      this.fetchData(id)
    }
    // Why need to make a copy of this.$route here?
    // Because if you enter this page and quickly switch tag, may be in the execution of the setTagsViewTitle function, this.$route is no longer pointing to the current page
    // https://github.com/PanJiaChen/vue-element-admin/issues/1221
    this.tempRoute = Object.assign({}, this.$route)  
  },
  methods: {
    checkPermission,
    addVul() {
      this.ticket_result.vulnerabilities.push({
          status: 0,
          vul_type: null,
          rank: null,
          url: "",
          description: "## 请详细填写漏洞详情",
          repair: "",
          key: Date.now()
      });
    },
    removeVul(item) {
      var index = this.ticket_result.vulnerabilities.indexOf(item)
      if (index !== -1) {
        this.ticket_result.vulnerabilities.splice(index, 1)
      }
    },
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
    fetchTranUser() {
      getTransactors().then(response => {
        if (!response.data) return
        this.userListOptions = response.data.map((user) => {
          var newUser = {};
          newUser['label'] = user.full_name;
          newUser['value'] = user.id;
          return newUser;
        })
      })
      getSecGroup().then(response => {
        if (!response.data) return
        this.SecUserListOptions = response.data.map((user) => {
          var newUser = {};
          newUser['label'] = user.full_name;
          newUser['value'] = user.id;
          return newUser;
        })
      })
    },
    fetchData(id) {
      getTicket(id).then(response => {
        this.postForm = response
        if (response.ticket_result) {
          this.ticket_result = response.ticket_result
        }   
        if (this.postForm.status === 1) {
          this.oldTransactors = this.postForm.transactors
          this.postForm.transactors = []
        }
        if (this.postForm.status === 3) {
          this.ticket_result = response.ticket_result
        }
        // set tagsview title
        // this.setTagsViewTitle()
        
        // set page title
        this.setPageTitle()
      })
    },
    setTagsViewTitle() {
      const title = 'Ticket Workflow'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    setPageTitle() {
      const title = 'Ticket Workflow'
      document.title = `${title} - ${this.postForm.id}`
    },
    onPass() {
      this.$refs.postForm.validate(valid => {
        if (this.postForm.status > 1 && this.ticket_result.vulnerabilities !== []) {
          for (let i=0; i < this.ticket_result.vulnerabilities.length; i++) {
            if(!validURL(this.ticket_result.vulnerabilities[i].url)){
              this.$message({
                message: `${this.ticket_result.vulnerabilities[i].url}不是有效的URL`,
                type: 'error',
                duration: 5 * 1000
              })
              return false
            }
          }
        }
        if (valid && this.postForm.transactors.length != 0) {
          this.loading = true
          if (this.postForm.status < 3) {
            if (this.postForm.status === 2) {
              createTicketResult(this.ticket_result).then(()=>{
                this.postForm.status += 1
                const id = this.$route.params.id
                editTicket(id, this.postForm).then(res => {
                  this.sub_workflow.action = '结束测试'
                  this.sub_workflow.workflow_description = "同意"
                  createSubWorkflow(this.sub_workflow).then(res => {
                    this.fetchData(this.$route.params.id)
                    this.$notify({
                      title: '成功',
                      message: '处理成功',
                      type: 'success',
                      duration: 2 * 1000
                    })
                    this.loading = false
                    if(this.postForm.status === 3) {
                      MessageBox.confirm('漏洞录入完成！请完善漏洞信息发起漏洞修复流', '处理漏洞流', {
                        confirmButtonText: '跳转',
                        cancelButtonText: '我知道了，稍后处理',
                        type: 'success'
                      }).then(() => {
                        this.$router.push({path: '/vuls/unactive'})
                      })
                    }
                  })
                })
              }).catch(err => {
                this.$notify({
                  title: '创建Ticket Result失败',
                  message: err,
                  type: 'error',
                  duration: 2 * 1000
                })
              })
            } else {
              this.postForm.status += 1
              const id = this.$route.params.id
              editTicket(id, this.postForm).then(res => {
                this.sub_workflow.action = '通过审核'
                let params = {id: res.id}
                penTodoNotifiy(params).then().catch()
                this.sub_workflow.workflow_description = "同意"
                createSubWorkflow(this.sub_workflow).then(res => {
                  this.fetchData(this.$route.params.id)
                  this.$notify({
                    title: '成功',
                    message: '处理成功',
                    type: 'success',
                    duration: 2 * 1000
                  })
                  this.loading = false
                })
              })
            }
          } else {
            this.$message({
              message: '流程错误！',
              type: 'error',
              duration: 2000
            })
          }
        } else {
          this.$message({
              message: '经办人为必填项目',
              type: 'error',
              duration: 2000
            })
          return false
        }
      })

    },
    onRefuse() {
      this.$refs.postForm.validate(valid => {
        if (valid && this.sub_workflow.workflow_description != '') {
          this.loading = true
          this.postForm.status = 0
          const id = this.$route.params.id
          this.postForm.transactors = this.oldTransactors
          editTicket(id, this.postForm).then(res => {
            this.sub_workflow.action = '拒绝工单'
            let params = {id: res.id}
            penTodoNotifiy(params).then().catch()
            createSubWorkflow(this.sub_workflow).then(res => {
              this.fetchData(this.$route.params.id)
              this.loading = false
              this.$notify({
                title: '拒绝',
                message: '处理成功',
                type: 'warning',
                duration: 2 * 1000
              })
            })
          })
        } else {
          this.$message({
              message: 'Submit Form Error | 拒绝时审批意见为必填',
              type: 'error',
              duration: 2000
            })
          return false
        }
      })
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
