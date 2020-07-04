<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">

      <sticky :z-index="10" :class-name="'sub-navbar '+ status[postForm.status]">
        <!-- <CommentDropdown v-model="postForm.comment_disabled" />
        <PlatformDropdown v-model="postForm.platforms" />
        <SourceUrlDropdown v-model="postForm.source_uri" /> -->
        <div  v-if="this.isEdit">
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="editForm(false)">
          更改
        </el-button>
        <el-button v-if="this.postForm.status != 0" v-loading="loading" type="warning" @click="backDraft">
          撤回流程(草稿)
        </el-button>
        <el-button v-else v-loading="loading" type="primary" @click="editForm(1)">
          发起流程
        </el-button>
        </div>
        <div v-else >
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          发起流程
        </el-button>
        <el-button v-loading="loading" type="warning" @click="draftForm">
          保存草稿
        </el-button>
        </div>
      </sticky>
      <div class="createPost-main-container">
        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 40px;" prop="title">
              <MDinput v-model="postForm.title" :maxlength="100" name="name" required>
                主题
              </MDinput>
            </el-form-item>
            <el-form-item v-if="this.isEdit" label-width="58px" label="创建人:" class="postInfo-container-item" prop="creator" >
              <el-input v-model="postForm.creator.full_name" :rows="1" type="textarea" class="article-textarea" :readonly="true" style="width: 15%; margin-bottom: 20px;"/>
            </el-form-item>
            <div class="postInfo-container">
              <el-row>
                <el-col :span="10">
                  <el-form-item label-width="58px" label="经办人:" class="postInfo-container-item" prop="transactors">
                    <el-select v-model="postForm.transactors" multiple  filterable default-first-option placeholder="Search User" >
                      <el-option v-for="item in userListOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :span="9">
                  <el-form-item label-width="120px" label="期望完成日期:" class="postInfo-container-item" prop="dead_line">
                    <el-date-picker v-model="displayTime" type="datetime" format="yyyy-MM-dd HH:mm:ss" placeholder="Select date and time" />
                  </el-form-item>
                </el-col>

                <el-col :span="5">
                  <el-form-item label-width="90px" label="优先级:" class="postInfo-container-item" prop="priority">
                    <el-rate
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
          <el-input v-model="postForm.department" :rows="1" type="textarea" class="article-textarea" placeholder="请填写全名" />
        </el-form-item>
        <el-alert
          :closable="false"
          title="需求详情"
          type="info"
          show-icon
        />
        <el-form-item style="margin-bottom: 10px;" prop="description" >
          <markdown-editor ref="markdownEditor" v-model="postForm.description" :language="'zh_CN'" height="500px" /> 
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' 
import MarkdownEditor from '@/components/MarkdownEditor'
import MDinput from '@/components/MDinput'
import Sticky from '@/components/Sticky' // 粘性header组件
import { validURL } from '@/utils/validate'
import { getTicket, newTicket, editTicket, createSubWorkflow, penTodoNotifiy } from '../../../api/universal'
import { getTransactors } from '../../../api/user'

const defaultForm = {
  status: 0,
  title: '',
  creator: '',
  priority: 1, // 优先级
  department: '',
  dead_line: '',
  description: '请务必填写完整1、项目背景。 2、需求。 3、必须的测试地址、测试账号。4、必要的其它信息',
  transactors: [],
}

export default {
  name: 'TicketDetail',
  components: { MarkdownEditor, MDinput, Sticky },
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
    // const validateSourceUri = (rule, value, callback) => {
    //   if (value) {
    //     if (validURL(value)) {
    //       callback()
    //     } else {
    //       this.$message({
    //         message: '外链url填写不正确',
    //         type: 'error'
    //       })
    //       callback(new Error('外链url填写不正确'))
    //     }
    //   } else {
    //     callback()
    //   }
    // }
    return {
      postForm: Object.assign({}, defaultForm),
      sub_workflow: {penetration_test_ticket: undefined, action: '发起流程', workflow_description: '无'},
      status: {0: 'draft', 1: 'publish'},
      loading: false,
      userListOptions: [],
      rules: {
        title: [{ validator: validateRequire, trigger: 'blur' }],
        description: [{ validator: validateRequire, trigger: 'blur' }],
        dead_line: [{ validator: validateRequire, trigger: 'blur' }],
        transactors: [{ validator: validateRequire, trigger: 'blur' }],
        department: [{ validator: validateRequire, trigger: 'blur' }],
        priority: [{ validator: validateRequire, trigger: 'blur' }]
        // source_uri: [{ validator: validateSourceUri, trigger: 'blur' }]
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
    }
  },
  created() {
    this.fetchTranUser()
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
    fetchTranUser() {
      getTransactors().then(response => {
        if (!response.data) return
        this.userListOptions = response.data.map((user) => {
          var newUser = {};
          newUser['label'] = user.full_name;
          newUser['value'] = user.id
          return newUser;
        })
      })
    },
    fetchData(id) {
      getTicket(id).then(response => {
        this.postForm = response
        // set tagsview title
        // this.setTagsViewTitle()
        
        // set page title
        this.setPageTitle()
      }).catch()
    },
    setTagsViewTitle() {
      const title = 'Edit Ticket'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    setPageTitle() {
      const title = 'Edit Ticket'
      document.title = `${title} - ${this.postForm.id}`
    },
    submitForm() {
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.postForm.status = 1
          newTicket(this.postForm).then(res => {
            this.sub_workflow.penetration_test_ticket = res.id
            this.sub_workflow.action = '发起流程'
            let params = {id: res.id}
            penTodoNotifiy(params).then().catch()
            createSubWorkflow(this.sub_workflow).then().catch()
            this.$notify({
              title: '成功',
              message: '开始审批流程',
              type: 'success',
              showClose: true,              
              duration: 2000
            })
          }).catch()
          this.loading = false
        } else {
          this.$message({
              message: 'Submit Form Error',
              type: 'error',
              duration: 2000
            })
          return false
        }
      })
    },
    draftForm() {
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.postForm.status = 0
          newTicket(this.postForm).then(res => {
            this.sub_workflow.penetration_test_ticket = res.id
            this.sub_workflow.action = '草稿'
            createSubWorkflow(this.sub_workflow).then(res => {
              this.$notify({
                title: '成功',
                message: '保存草稿成功',
                type: 'success',
                showClose: true,
                duration: 2000
              })
            }).catch()
          }).catch()
          this.loading = false
        } else {
          this.$message({
              message: '表单填写有误！',
              type: 'error',
              duration: 2000
            })
          return false
        }
      })
    },
    backDraft() {
      if (this.isEdit) {
        const id = this.$route.params && this.$route.params.id
        this.$confirm('确认撤回工单?撤回后工单将退回草稿状态！', '撤回工单', {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.postForm.status = 0
          delete this.postForm.sub_workflow
          editTicket(id, this.postForm).then(res => {
            this.sub_workflow.penetration_test_ticket = res.id
            this.sub_workflow.action = '退回草稿'
            createSubWorkflow(this.sub_workflow).then(res => {
            }).catch()
            this.$notify({
              title: '成功',
              message: '撤回成功',
              type: 'success',
              duration: 2 * 1000
            })
          }).catch()
        })
      }
    },
    editForm(status) {
      if (this.isEdit) {
        const id = this.$route.params && this.$route.params.id
        if (status) {
          if (this.postForm.status > status) {
            this.sub_workflow.action = '退回草稿'
          } else if (this.postForm.status < status ){
            this.sub_workflow.action = '发起流程'
          } else {
            this.sub_workflow.action = '编辑'
          }
          this.postForm.status = status
        }
        delete this.postForm.sub_workflow
        editTicket(id, this.postForm).then(res => {
          this.sub_workflow.penetration_test_ticket = res.id
          if (res.status === 1) {
            let params = {id: res.id}
            penTodoNotifiy(params).then().catch()
          }
          createSubWorkflow(this.sub_workflow).then(res => {
          }).catch(error => {
            this.$message({
              message: error || 'Error',
              type: 'error',
              duration: 5 * 1000
            })
          })
          this.$notify({
            title: '成功',
            message: '修改成功',
            type: 'success',
            duration: 2 * 1000
          })
        }).catch()
      }
    }
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
