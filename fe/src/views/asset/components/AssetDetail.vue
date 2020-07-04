<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">

      <sticky :z-index="10" :class-name="'sub-navbar '+ status[isEdit]">
        <!-- <CommentDropdown v-model="postForm.comment_disabled" />
        <PlatformDropdown v-model="postForm.platforms" />
        <SourceUrlDropdown v-model="postForm.source_uri" /> -->
        <div v-if="isEdit">
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="editForm">
          更改
        </el-button>
        </div>
        <div v-else>
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          保存
        </el-button>
        </div>
      </sticky>
      <div class="createPost-main-container">
        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 40px;" prop="name">
              <MDinput v-model="postForm.name" :maxlength="100" name="name" required>
                资产名称
              </MDinput>
            </el-form-item>
            <div class="postInfo-container">
              <el-row>
                <el-col :span="12">
                  <el-form-item  label-width="45px" label="域名:" prop="domain" style="margin-bottom: 40px;">
                    <el-input v-model="postForm.domain" :rows="1" type="textarea" class="article-textarea" placeholder="请填写资产域名" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item  label-width="73px" label="IP地址:" prop="ip" style="margin-bottom: 40px;">
                    <el-input v-model="postForm.ip" :rows="1" type="textarea" class="article-textarea" placeholder="请填写资产ip地址" />
                  </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label-width="87px" label="资产负责人:" class="postInfo-container-item" prop="pics">
                    <el-select v-model="postForm.pics" filterable multiple placeholder="Search User" style="width: 250%">
                      <el-option v-for="item in userListOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-card v-for="port in postForm.ports" :key="port.key" shadow="hover" style="margin-bottom: 10px;"  >
                <div slot="header" class="clearfix">
                  <span>端口信息</span>
                    <el-button style="float: right;  padding: 3px 3px" type="danger" @click="removePort(port)" circle icon="el-icon-delete"></el-button>
                </div>
                <el-row>
                  <el-col :span="7">
                    <el-form-item label-width="73px" label="端口号:" prop="port" style="margin-bottom: 40px;">
                      <el-input v-model="port.port" type="number"/>
                    </el-form-item>
                    </el-col>
                  <el-col :span="7">
                      <el-form-item label-width="73px" label="服务:" class="postInfo-container-item" prop="service">
                        <el-input v-model="port.service" :rows="1" type="textarea" class="article-textarea" /> 
                      </el-form-item>
                  </el-col>
                  <el-col :span="7">
                      <el-form-item label-width="73px" label="版本号:" class="postInfo-container-item" prop="version">
                        <el-input v-model="port.version" :rows="1" type="textarea" class="article-textarea" /> 
                      </el-form-item>
                  </el-col>
                  <el-col :span="24">
                      <el-form-item label-width="73px" label="脆弱信息:" class="postInfo-container-item" prop="vulnerable" style="width: 100%">
                        <el-input v-model="port.vulnerable" :rows="1" type="textarea" class="article-textarea" /> 
                      </el-form-item>
                  </el-col>
                </el-row>
              </el-card>
              <el-button type="info" size="mini" icon="el-icon-plus" @click="addPort" style="margin-bottom: 20px;">新增端口</el-button>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import MDinput from '@/components/MDinput'
import Sticky from '@/components/Sticky' // 粘性header组件
import { validURL } from '@/utils/validate'
import { getTransactors, getUsers, getUserInfo } from '../../../api/user'
import { newAsset, editAsset, getAsset, deletePort, editPort } from '../../../api/universal'
import { MessageBox } from 'element-ui'

const defaultForm = {
  name: '',
  domain: '',
  ip: '',
  pics: [],
  info: '',
  ports: [],
}

export default {
  name: 'AssetDetail',
  components: { MDinput, Sticky },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    },
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
    const validatePort = (rule, value, callback) => {
      if (value > 1 && value <= 65535) {
          this.$message({
            message: '端口号填写不正确',
            type: 'error'
          })
          callback()
      } else {
        callback(new Error('端口号填写不正确'))
      }
    }
    return {
      postForm: Object.assign({}, defaultForm),
      loading: false,
      userListOptions: [],
      status: {false: 'draft', true: 'publish'},
      rules: {
        name: [{ validator: validateRequire, trigger: 'blur' }],
        ip: [{ validator: validateRequire, trigger: 'blur' }],
        pics: [{ validator: validateRequire, trigger: 'blur' }],
        // port: [{ validator: validatePort, trigger: 'blur' }],
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
    this.fetchUsers()
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
    fetchUsers() {
      getUsers().then(response => {
        this.userListOptions = response.results.map((user) => {
          var newUsers = {};
          newUsers['label'] = user.full_name;
          newUsers['value'] = user.id;
          return newUsers;
        })
      })
    },
    fetchData(id) {
      getAsset(id).then(response => {
        this.postForm = response
      })
    },
    addPort() {
      this.postForm.ports.push({
          port: null,
          service: "",
          version: "",
          vulnerable: "",
          key: Date.now()
      });
    },
    removePort(item) {
      if (this.isEdit) {
        MessageBox.confirm('确认要删除?端口将立即删除！', '确认删除', {
          confirmButtonText: '是的',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deletePort(item.id).then(() => {
            MessageBox({
              message: '删除成功',
              type: 'info',
              duration: 2 * 1000
            })
            var index = this.postForm.ports.indexOf(item)
            if (index !== -1) {
              this.postForm.ports.splice(index, 1)
            }
          })
        })
      } else {
        var index = this.postForm.ports.indexOf(item)
        if (index !== -1) {
          this.postForm.ports.splice(index, 1)
        }
      }
    },
    setTagsViewTitle() {
      const title = 'Edit Asset'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    setPageTitle() {
      const title = 'Edit Asset'
      document.title = `${title} - ${this.postForm.id}`
    },
    submitForm() {
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.loading = true
          newAsset(this.postForm).then(() => {
            this.$notify({
              title: '成功',
              message: '新建了一个新的资产',
              type: 'success',
              duration: 2 * 1000
            })
            this.$router.push({path: '/asset/all'})
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
        editAsset(id, this.postForm).then(() => {
          this.$notify({
            title: '成功',
            message: '修改资产成功',
            type: 'success',
            duration: 2 * 1000
          })
          for (let i=0; i < this.postForm.ports.length; i++) {
            editPort(this.postForm.ports[i].id, this.postForm.ports[i]).then().catch()
          }
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
