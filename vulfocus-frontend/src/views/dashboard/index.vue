<template>

  <div class="dashboard-container">
    <el-row :gutter="20" >
      <el-dialog :visible.sync="centerDialogVisible" title="镜像信息" >
        <div class="text item" v-loading="startCon" element-loading-text="环境启动中">
          访问地址: {{vul_host}}
        </div>
        <div class="text item">
          名称: {{images_name}}
        </div>
        <div class="text item">
          描述: {{images_desc}}
        </div>
        <el-form>
          <el-form-item label="Flag">
            <el-input v-model="input" placeholder="请输入Flag：格式flag-{xxxxxxxx}"></el-input>
          </el-form-item>
          <el-form-item>
            <!--<div slot="footer" class="dialog-footer">-->
            <el-button type="primary" @click="subflag(container_id,input.trim())" :disabled="Cstatus">提 交</el-button>
            <!--</div>-->
          </el-form-item>
        </el-form>
      </el-dialog>
      <el-col>
        <el-input v-model="search" style="width: 230px;" size="medium"></el-input>
        <el-button class="filter-item" size="medium" style="margin-left: 10px;margin-bottom: 10px" type="primary" icon="el-icon-search" @click="handleQuery">
          查询
        </el-button>
      </el-col>
      <el-col :span="6" v-for="(item,index) in listdata" :key="index"  style="padding-bottom: 18px;">
        <el-card :body-style="{ padding: '8px' }" shadow="hover"
                 @click.native=" item.status.status === 'running' && open(item.image_id,item.image_vul_name,item.image_desc,item.status.status,item.status.container_id,item)" >
          <div class="clearfix" >
          <svg-icon icon-class="bug"  style="font-size: 20px;"/>
            <div style="display: inline-block;color: #20a0ff" >
              <i v-if="item.status.status && item.status.is_check" class="el-icon-check"></i>
              <i v-else-if="item.status.status === 'running'" class="el-icon-loading"></i>
            </div>
            <el-rate
              v-model=item.rank
              disabled
              show-score
              text-color="#ff9900"
              score-template={value}>
            </el-rate>
          </div>
          <div style="padding: 5px;" >
            <div class="container-title">
            <span>{{item.image_vul_name}}</span>
            </div>
            <div class="bottom clearfix">
              <div class="time container-title">{{ item.image_desc }}</div>
            </div>
            <el-row>
              <el-button type="primary" @click.stop="Stop(item.status.container_id,item)" size="mini "v-if="item.status.status === 'running'">停止</el-button>
              <el-button type="primary" @click.stop="open(item.image_id,item.image_vul_name,item.image_desc,item.status.status,item.status.container_id,item)" size="mini" v-else="item.status.status === '' || item.status.status === 'stop'">启动</el-button>
              <el-button type="primary" @click.stop="Delete(item.status.container_id,item)" v-if="item.status.status === 'running'" size="mini" icon="el-icon-stopwatch">删除</el-button>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ImgList,ContainerSTATUS,SubFlag,ContainerSTART,ContainerDelete,ContainerStop,ContainerStart } from '@/api/docker'
import Message from 'element-ui/packages/message/src/main'

export default {
  name: 'Dashboard',
    data() {
      return {
          listdata: [],
          vul_host: "",
          centerDialogVisible: false,
          startCon:false,
          input: "",
          images_id: "",
          container_id: "",
          images_name: "",
          images_desc: "",
          item_raw_data: "",
          Cstatus: false,
          search: ""
       };
    },
    created() {
      this.ListData()
    },
  methods:{
      ListData() {
          ImgList().then(response => {
              this.listdata = response.data
          })
      },
      Cifno(id,raw_data){
        ContainerSTATUS(id).then(response => {
          let container_status = response.data.container_status
          if(container_status === 'stop'){
            // 启动
            ContainerStart(id).then(response=>{
              if(response.status===201){
                this.vul_host = response.data.info
                this.container_id = id
                raw_data.status.status = 'running'
                raw_data.status.container_id = container_id
                this.startCon = false
                this.Cstatus = false
              }
            })
          }else if(container_status === 'running'){
            this.vul_host = response.data.vul_host
          }
        })
      },
      open(id,images_name,images_desc,status,container_id,raw_data) {
          this.images_id = ''
          this.images_name = ''
          this.images_desc = ''
          this.container_id = ''
          this.item_raw_data = ''
          this.startCon = 'loading'
          this.item_raw_data = raw_data
          this.images_id = id
          this.images_name = images_name
          this.images_desc = images_desc
          this.centerDialogVisible = true
          if(raw_data.status.is_check === true){
            this.$message({
              message:  '该题目已经通过',
              type: 'success',
            })
            this.centerDialogVisible = false
          }
          ContainerSTART(id).then(response=>{
            if(response.status===201){
              container_id = response.data.container_id;
              this.container_id = container_id;
              this.vul_host = response.data.info
              raw_data.status.status = 'running'
              raw_data.status.container_id = container_id
              this.startCon = false
              this.Cstatus = false
              this.container_id = container_id
            }else if(response.status === 202){
              this.$message({
                message: response.data.msg,
                type: 'info',
              })
            }else {
              this.$message({message:  response.data.msg,
                type: 'error',
              })
              this.centerDialogVisible = false
            }
          })
      },
      subflag(id,flag) {
          SubFlag(id,flag).then(response => {
            if (response.data.code === "2002"|| response.data.code === "2003" || response.data.code === '2001') {
              this.$message({
                message:  'Flag错误',
                type: 'error',
              })
            }
            if (response.data.code === "2000") {
              this.$message({
                message:  '恭喜！通过',
                type: 'success',
              })
            }
            this.centerDialogVisible = false
            this.item_raw_data.status.status = 'stop'
          })

      },
      Stop(container_id,raw) {
        /**
         * 停止容器运行
         */
        ContainerStop(container_id).then(response=>{
          if(response.status === 201){
            this.$message({
              message: response.data.msg,
              type: 'success',
            })
            raw.status.status = 'stop'
          }else{
            this.$message({
              message: '容器停止失败',
              type: 'error',
            })
          }
        })
      },
      Delete(container_id,raw){
        /**
         * 删除容器
         */
        ContainerDelete(container_id).then(response=>{
          if(response.status === 201){
            // 清空状态码
            raw.status.status = ''
            // 清空 image_id
            this.images_id = ''
            // 清空 image_name
            this.images_name = ''
            // 清空 image_desc
            this.images_desc = ''
            // 清空 container_id
            this.container_id = ''
            // 清空 item_raw_data
            this.item_raw_data = ''
            raw.status.container_id = ''
            this.$message({
              message: response.data.msg,
              type: 'success',
            })
          }else{
            this.$message({
              message: '容器删除失败',
              type: 'error',
            })
          }
        })
      },
      handleQuery(){
        ImgList(this.search).then(response => {
          this.listdata = response.data
        })
      }
  }


}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 5px;
  margin-bottom: 13px;
  line-height: 12px;
}

.button {
  padding: 5;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.container-title{
  width: 100%;    /*根据自己项目进行定义宽度*/
  overflow: hidden;     /*设置超出的部分进行影藏*/
  text-overflow: ellipsis;     /*设置超出部分使用省略号*/
  white-space:nowrap ;    /*设置为单行*/
}
</style>
