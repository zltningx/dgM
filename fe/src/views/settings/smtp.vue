<template>
  <div>
    <el-card shadow="never">
      <div slot="header" class="clearfix">
        <span style="font-weight:bold; font-size: 20px;">SMTP 配置</span>
      </div>
      <el-form ref="smtpForm" :model="smtpForm" :rules="rules" class="form-container">
        <el-form-item label="SMTP 服务器地址:" label-width="150px" prop="server">
          <el-input v-model="smtpForm.server" style="width: 400px;" placeholder="请输入服务器地址"/> ：
          <el-input v-model="smtpForm.port" style="width: 100px" />
        </el-form-item>
        <el-form-item label="发件邮箱帐号:" label-width="150px" prop="username">
          <el-input v-model="smtpForm.username" style="width: 400px;" placeholder="请输入邮箱地址"/>
        </el-form-item>
        <el-form-item label="发件邮箱smtp密码:" label-width="150px" prop="password" >
          <el-input 
          v-model="smtpForm.password"
          show-password
          style="width: 400px;"
          placeholder="请输入密码"/>
        </el-form-item>
        <el-form-item label="加密方法:" prop="encryption_method" label-width="150px">
          <el-radio-group v-model="smtpForm.encryption_method" style="width: 400px;">
            <el-radio label="NONE"></el-radio>
            <el-radio label="SSL"></el-radio>
            <el-radio label="TLS"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="邮箱签名:" label-width="150px" prop="signature">
          <el-input v-model="smtpForm.signature" :rows="1" type="textarea" autosize style="width: 400px;" placeholder="请输入邮箱签名内容"/>
        </el-form-item>
        <el-form-item label="测试邮件地址:" label-width="150px" prop="signature">
          <el-input v-model="testEmail" style="width: 400px;" placeholder="如需测试，请填写测试邮件接受邮件地址"/>
        </el-form-item>
        <el-form-item label-width="150px">
          <el-button v-if="isExists" type="primary" @click="updateForm()">更新配置</el-button>
          <el-button v-else type="primary" @click="submitForm()">添加配置</el-button>
          <el-button v-if="isExists" type="danger" @click="testConfig()">发送测试邮件</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getSMTPConfig, newSMTPConfig, editSMTPConfig, testSMTPConfig } from '../../api/universal'

export default {
  name: 'SMTPConfig',
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
      smtpForm: {
        server: '',
        port: 1,
        username: '',
        password: '',
        encryption_method: '',
        signature: '',
      },
      testEmail: '',
      isExists: false,
      loading: false,
      redirect: undefined,
      rules: {
        server: [{ validator: validateRequire, trigger: 'blur' }],
        username: [{ validator: validateRequire, trigger: 'blur' }],
        password: [{ validator: validateRequire, trigger: 'blur' }],
        encryption_method: [{ validator: validateRequire, trigger: 'blur' }]
      }
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getSMTPConfig().then(res => {
        if (res.results.length !== 0) {
          this.smtpForm = res.results[0]
          this.isExists = true
        }
      })
    },
    submitForm() {
      this.smtpForm.port = parseInt(this.smtpForm.port)
      newSMTPConfig(this.smtpForm).then(() => {
        this.$notify({
          title: '成功',
          message: '保存成功，可以使用系统邮件功能了！',
          type: 'success',
          showClose: true,              
          duration: 2000
        })
      }).catch()
    },
    updateForm() {
      this.smtpForm.port = parseInt(this.smtpForm.port)
      editSMTPConfig(this.smtpForm.id, this.smtpForm).then(() => {
        this.$notify({
          title: '成功',
          message: '修改成功！',
          type: 'success',
          showClose: true,              
          duration: 2000
        })
      }).catch()
    },
    testConfig() {
      if (this.testEmail !== '') {
        let form = {'email': this.testEmail}
        testSMTPConfig(form).then(() => {
        this.$notify({
          title: '成功',
          message: '测试邮件发送成功',
          type: 'success',
          showClose: true,              
          duration: 2000
        })
        }).catch()
      } else {
        this.$notify({
          title: '失败',
          message: '未填写测试邮件地址',
          type: 'error',
          showClose: true,              
          duration: 3000
        })
      }
    },
  }
}
</script>

<style lang="scss" scoped>
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

</style>