<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">

      <sticky :z-index="10" :class-name="'sub-navbar '+ status[postForm.status]">
        <!-- <CommentDropdown v-model="postForm.comment_disabled" />
        <PlatformDropdown v-model="postForm.platforms" />
        <SourceUrlDropdown v-model="postForm.source_uri" /> -->
        <div  v-if="this.isEdit && this.completed">
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="editForm">
          更改
        </el-button>
        </div>
        <div v-else-if="this.completed" >
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          发起修复流
        </el-button>
        </div>
        <div v-else>
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="completeForm">
          发起修复流
        </el-button>
        </div>
      </sticky>
      <div class="createPost-main-container">
        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 40px;" prop="title">
              <MDinput v-model="postForm.title" :maxlength="100" name="name" required>
                标题
              </MDinput>
            </el-form-item>
            <!-- <el-form-item v-if="this.isEdit" label-width="58px" label="创建人:" class="postInfo-container-item" prop="creator" >
              <el-input v-model="postForm.creator.full_name" :rows="1" type="textarea" class="article-textarea" :readonly="true" style="width: 15%; margin-bottom: 20px;"/>
            </el-form-item> -->
            <div class="postInfo-container">
              <el-row>
                <el-col :span="8">
                    <el-form-item label-width="73px" label="漏洞类型:" class="postInfo-container-item" prop="vul_type">
                      <el-select v-model="postForm.vul_type" filterable default-first-option placeholder="Search Type"   >
                        <el-option v-for="item in vulTypes" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label-width="73px" label="关联资产:" class="postInfo-container-item" prop="asset">
                    <el-select v-model="postForm.asset" filterable default-first-option placeholder="Search Asset" >
                      <el-option v-for="item in assetOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label-width="73px" label="漏洞等级:" class="postInfo-container-item" prop="rank">
                      <el-select v-model="postForm.rank">
                        <el-option v-for="item in ranks" :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item  label-width="73px" label="漏洞链接:" prop="url" style="margin-bottom: 40px;">
                    <el-input v-model="postForm.url" :rows="1" type="textarea" class="article-textarea" placeholder="请填写漏洞URL" />
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
        <el-form-item prop="description" >
          <markdown-editor ref="MarkdownEditor" v-model="postForm.description"  height="500px" /> 
        </el-form-item>
        <el-form-item label-width="73px" label="修复方案:" prop="repair" style="margin-bottom: 40px">
          <el-input v-model="postForm.repair" type="textarea" autosize placeholder="请详细填写方案" />
        </el-form-item>
        <el-form-item label-width="48px" label="来源:" prop="resource" style="margin-bottom: 40px">
          <el-select v-model="postForm.resource">
            <el-option v-for="item in resources" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
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
import { getVulTypes, getAssets, newVulWorkflow, getVulWorkflow, getVul, editVulWorkflow, vulTodoNotifiy, createVulSubWorkflow, editVul } from '../../../api/universal'
import { getTransactors } from '../../../api/user'

const defaultForm = {
  status: 0,
  title: '',
  asset: '',
  vul_type: '',
  rank: '',
  url: '',
  description: '',
  repair: '',
  resource: ''
}

export default {
  name: 'VulDetail',
  components: { MarkdownEditor, MDinput, Sticky },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    },
    completed: {
      type: Boolean,
      default: true
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
    const validateUri = (rule, value, callback) => {
      if (value) {
        if (validURL(value)) {
          callback()
        } else {
          this.$message({
            message: 'url填写不正确',
            type: 'error'
          })
          callback(new Error('url填写不正确'))
        }
      } else {
        callback(new Error('url填写不正确'))
      }
    }
    return {
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
      sub_workflow: {vul_workflow: undefined, action: '发起流程', workflow_description: '无'},
      status: {0: 'draft', 1: 'publish'},
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
      rules: {
        title: [{ validator: validateRequire, trigger: 'blur' }],
        vul_type: [{ validator: validateRequire, trigger: 'blur' }],
        asset: [{ validator: validateRequire, trigger: 'blur' }],
        rank: [{ validator: validateRequire, trigger: 'blur' }],
        url: [{ validator: validateUri, trigger: 'blur' }],
        description: [{ validator: validateRequire, trigger: 'blur' }],
        repair: [{ validator: validateRequire, trigger: 'blur' }],
        resource: [{ validator: validateRequire, trigger: 'blur' }]
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
    this.fetchVulTypes()
    this.fetchAssets()
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
      if (this.completed) {
        getVulWorkflow(id).then(response => {
          this.postForm.title = response.title
          this.postForm.asset = response.asset
          this.postForm.resource = response.resource
          this.postForm.vul_type = response.vulnerability.vul_type
          this.postForm.rank = response.vulnerability.rank 
          this.postForm.url = response.vulnerability.url
          this.postForm.description = response.vulnerability.description
          this.postForm.repair = response.vulnerability.repair
          // set tagsview title
          // this.setTagsViewTitle()
          
          // set page title
          // this.setPageTitle()
        })
      } else {
        getVul(id).then(response => {
          this.postForm = response
          // set tagsview title
          // this.setTagsViewTitle()
          
          // set page title
          // this.setPageTitle()
        })
      }
    },

    setTagsViewTitle() {
      if(this.completed){
        const title = 'Edit Ticket'
      } else {
        const title = 'Complete Ticket'
      }
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    setPageTitle() {
      if(this.completed){
        const title = 'Edit Ticket'
      } else {
        const title = 'Complete Ticket'
      }
      document.title = `${title} - ${this.postForm.id}`
    },
    setNewForm() {
      this.newForm.title = this.postForm.title
      this.newForm.asset = this.postForm.asset
      this.newForm.resource = this.postForm.resource
      this.newForm.vulnerability.vul_type = this.postForm.vul_type
      this.newForm.vulnerability.rank = this.postForm.rank
      this.newForm.vulnerability.url = this.postForm.url
      this.newForm.vulnerability.description = this.postForm.description
      this.newForm.vulnerability.repair = this.postForm.repair
    },
    submitForm() {
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.setNewForm()
          newVulWorkflow(this.newForm).then(res => {
            this.sub_workflow.vul_workflow = res.id
            this.sub_workflow.action = '发起修复流程'
            let params = {id: res.id, message: ''}
            vulTodoNotifiy(params).then().catch()
            createVulSubWorkflow(this.sub_workflow).then().catch()
            this.$notify({
              title: '成功',
              message: '开始修复流程',
              type: 'success',
              showClose: true,
              duration: 2000
            })
          })
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
    completeForm() {
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.setNewForm()
          delete this.newForm['vulnerability']
          delete this.postForm['asset']
          delete this.postForm['title']
          delete this.postForm['resource']
          newVulWorkflow(this.newForm).then(res => {
            this.postForm.vul_workflow = res.id
            this.postForm.status = 1
            editVul(this.postForm.id, this.postForm).then(()=>{
              let params = {id: this.postForm.vul_workflow, message: ''}
              vulTodoNotifiy(params).then().catch()
            }).catch()
            this.sub_workflow.vul_workflow = res.id
            this.sub_workflow.action = '发起修复流程'
            createVulSubWorkflow(this.sub_workflow).then().catch()
            this.$notify({
              title: '成功',
              message: '开始修复流程',
              type: 'success',
              showClose: true,
              duration: 2000
            })
          })
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
    editForm() {
      if (this.isEdit) {
        const id = this.$route.params && this.$route.params.id
        // if (status) {
        //   if (this.postForm.status > status) {
        //     this.sub_workflow.action = '退回草稿'
        //   } else if (this.postForm.status < status ){
        //     this.sub_workflow.action = '发起流程'
        //   } else {
        //     this.sub_workflow.action = '编辑'
        //   }
        //   this.postForm.status = status
        // }
        // delete this.postForm.sub_workflow
        this.setNewForm()
        editVulWorkflow(id, this.newForm).then(res => {
        //   this.sub_workflow.penetration_test_ticket = res.id
        //   createSubWorkflow(this.sub_workflow).then(res => {
        //   }).catch(error => {
        //     this.$message({
        //       message: error || 'Error',
        //       type: 'error',
        //       duration: 5 * 1000
        //     })
        //   })
          this.$notify({
            title: '成功',
            message: '修改成功',
            type: 'success',
            duration: 2 * 1000
          })
        })
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
