   

//  pod ���ݰ󶨱����
    var alldata = []  ;
    var hasPort = new Array() ;

     /* ������port ����*/
     function cachePort(port){
        var strPort = hasPort.join(",");
        if(strPort.indexOf(port) != -1 ){
            return  ;
        }else{
            hasPort.push(port);
        }

     }

      function checkP(){
      }

      function setFrameSrc(src){
       iframe =  $("#podRes");
       iframe.attr("src",src);
      }
        // onclick-RC-Row
      function loadPodByLable(index,row){
         podstatusURI =  ":4194/containers/docker/";
            alldata=[];
            api = url+getpods.replace("default",row.namespace)+"?labelSelector=name="+row.rclable ;
            $.ajax({
                url: api,
                type:"get",
                dataType:"json",
                async:false,
                success: function(data){
                    $.each(data.items,function(i,item){
                        var drow = {};
                        drow.name = item.metadata.name ;
                        drow.status = item.status.phase ;
                        var hostip = item.status.hostIP;
                        var containerip =item.status.podIP;

                        drow.starttime = item.status.startTime ;

                            drow.hostip  = hostip ;
                            drow.containerip = containerip ;
                        alldata.push(drow) ;

                    });

                },
                error:function(){
                    alert("��ȡPODʱ�������쳣����ˢ��ҳ������!");

                }
            });


            $('#dg').datagrid({
              data:alldata,
              onClickRow:loadPodDetailByName,
            });

        }

    function loadAllPods(ns){
        alldata_pod=[];
        
        console.log(url) ;
        if(url.indexOf("K8s") != -1){
        	api = url ;
        }else{
        	api =  url+"K8s" ;
        }
        
        $.ajax({
            url: api,
            type:"get",
            dataType:"json",
            async:false,
            success: function(data){
                $.each(data.items,function(i,item){
                    var drow = {};
                    drow.name = item.metadata.name ;
                    drow.status = item.status.phase ;
                    drow.app_status = item.status.containerStatuses[0].ready ;
                    var hostip = item.status.hostIP;
                    var containerip =item.status.podIP;
                    //�Լ�������ʱ��
                    drow.age = item.metadata.age;
                    drow.cpu = item.metadata.cpu;
                    drow.mem = item.metadata.mem;
                    drow.starttime = item.status.startTime ;

                       drow.hostip  = hostip ;
                       drow.containerip = containerip ;
                    alldata_pod.push(drow) ;

                });

            },
            error:function(){
                alert("��ȡPODʱ�������쳣����ˢ��ҳ������!,�����ַ=="+url+"?labels=name="+row.rclable);
            }
        });


        $('#dg').datagrid({
            data:alldata,
            onClickRow:loadPodDetailByName,
        });

        $('#pod_dg').datagrid({
            data:alldata_pod,
            onClickRow:loadPodDetailByName,
        });

    }

       function loadPodDetailByName(){


       }

        /** ����RC **/
        function newRC(){
              $('#dlg').dialog('open').dialog('center').dialog('setTitle','����һ������');
              $('#fm').form('clear');

              /**ports =  $('input[name*="cspor"]') ;
              for (var i = 0 ; i<ports.length ; i++) {
                 ports[i].bind('blur',checkPort()) ;
              }**/
        }


        function GetJsonData(namespace,name,replicas,selector,image,sport,dport,commandline,args){

            //ȡ����������sshӳ��˿�
            var sshport = getPort() ;

            var RC =  {

                  "kind": "ReplicationController",
                  "apiVersion": "v1",
                  "metadata": {
                    "name": name,
                    "namespace": namespace,
                  },
                  "spec":{
                      "replicas":replicas,
                      "selector":{
                         "name":selector
                    },
                  "template":{
                     "metadata":{
                     "namespace": namespace,
                        "labels":{
                           "name":selector
                        }
                     },
                     "spec":{
                        "volumes": [
                                {
                                "name": "nfs",
                                "hostPath": {"path": "/mnt/nfs"}
                                }
                            ],
                        "containers":[
                           {
                              "name":name,
                              "image":image,
                            /**"command": [
                              commandline
                            ],
                            "args": [
                              args
                            ],**/
                              "ports": [
                                  /**{
                                    "hostPort": sport,
                                    "containerPort":dport, 
                                    "protocol": "TCP"
                                  },**/
                                  {
                                    "hostPort": sshport,
                                    "containerPort":22,
                                    "protocol": "TCP"
                                  }
                                ],
                                "volumeMounts": [
                                     {
                                        "name": "nfs",
                                        "readOnly": false,
                                        "mountPath": "/mnt"
                                    }
                                ],
                           }
                        ]
                     }
                  },

               }
            } /*end RC */

            return RC ;
        }

       function getPort(){
          var port = 22222 ;
          $.ajax({
                      url: url+getport,
                      type:"get",
                      dataType:"json",
                      async:false,
                      success: function(data){
                          port = parseInt(data) ;
                      },
                      error:function(){
                          alert("ȡ����������ӳ��˿�ʧ��!");
                      }
          });

          return port ;

       }


   


    function delRC(){

                var row = $('#rc').datagrid('getSelected');

                if (row){
                    $.messager.confirm('Confirm','��ȷ��Ҫ������?',function(r){
                      //del rc
                        $.ajax({
                            url: url+get_rc+"/"+row.rcname,
                            type:"DELETE",
                            dataType:"json",
                           // async:true,
                            success: function(data){
                               alert("ɾ���ɹ�!");
                               loadRC();
                                alldata = []  ;
                                 $('#dg').datagrid({
                                          data:alldata,
                                          onClickRow:loadPodDetailByName,
                                });
                               $('#rc').datagrid('reload');
                            },
                            error:function(){
                                alert("ɾ��RCʱ�������쳣����ˢ��ҳ������!");
                            }
                        });//del rc end

                     });

                  }
        }

    //�洢server ���ص�rc json ��ȥ�������server��״̬��Ϣ������ʱ�����Ϣ
    var RC_JOSN=[] ;
    function getRC_JSON(response_json) {
        rc_obj={} ;
        //add  attribute
        response_json.kind = "ReplicationController" ;
        response_json.apiVersion = "v1" ;

        //del attribute
        delete response_json.metadata.creationTimestamp;
        delete response_json.metadata.generation;
        delete response_json.metadata.resourceVersion;
        delete response_json.metadata.selfLink ;
        delete response_json.metadata.uid;

        delete response_json.spec.template.metadata.creationTimestamp;
        delete response_json.spec.template.spec.containers[0].terminationMessagePath;
        delete response_json.spec.template.spec.containers[0].terminationMessagePolicy;

        delete response_json.spec.template.spec.schedulerName ;
        delete response_json.spec.template.spec.dnsPolicy ;
        delete response_json.spec.template.spec.securityContext ;
        delete response_json.spec.template.spec.terminationGracePeriodSeconds ;
//        delete response_json.spec.template.spec.terminationGracePeriodSeconds ;
        delete response_json.status ;

        rc_obj.rcname = response_json.metadata.name;
        rc_obj.json=response_json ;
        //get current replicas
        rc_obj.replicas=response_json.spec.replicas ;
        rc_obj.namespace = response_json.metadata.namespace ;

        RC_JOSN.push(rc_obj) ;
//        console.log(response_json) ;

//        $.each(response_json.spec.template.spec.containers,function(i,item){
//            console.log(item.image);
//        })
    }

    //scaleUP RC
    // +1
    function addRC_Number(rc_json) {
//        console.log(rc_json.json.spec.replicas)

        rc_json.json.spec.replicas =   parseInt(rc_json.replicas)+ 1 ;
        api = url +  get_rc.replace("default",rc_json.namespace) + "/" + rc_json.rcname;

        $.ajax({
            url: api,
            type:"put",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(rc_json.json),
            dataType:"json",
            async:false,
            success: function(data){
		   alert('scaleUP ok'); 
                    console.log(data) ;
            },
            error:function(){
                alert("scale UP ʱ�������쳣!");
            }
        });

    }

   

    function getResource(namespace){
        //loadRC(namespace);
        loadAllPods(namespace);	
    }

    /*���port �Ƿ��Ѿ�ʹ�� false:ʹ��    true:û��ʹ��*/
    function checkPort(sport){

        //����ʹ��
        var flag = true ;

          $.ajax({
                url: url+getport+sport,
                type:"get",
                success: function(data){
                    //alert(data);
                    if(data == "True") {
                        flag = false ;
                    }
                },
                error:function(){
                    alert("���˿��Ƿ�ռ��ʧ��!"+ (url+getport+sport));
                }
            });


        return flag ;

   }

   //��������Ƿ���ʹ��
   function checkRCName(rcname){
        var flag = true ;
        $.each(rc_data,function(i,data){
             if(data.rcname == rcname){
                 alert("�������� ��"+ rcname +"�� ��ʹ��,���������.");
                 flag = false ;
                 return false;
             }
        })
        return flag ;
   }

    function addPort(){
        var fm  = $("#port") ;
        $('<div/>',{
        id:'test1',
        "class":"fitem",
        }).appendTo(fm);

        $("<span class=\"textbox textbox-invalid numberbox\" style=\"width: 68px; height: 20px;margin-left: 82px;\"><input name=\"csport\" class=\"textbox-text validatebox-text textbox-prompt validatebox-invalid\"  min=\"1024\" max=\"65535\" required style=\"width: 60px;border-color: #ffa8a8;\"></span> : <span class=\"textbox textbox-invalid numberbox\" style=\"width: 68px; height: 20px;\"><input name=\"cdport\" class=\"textbox-text validatebox-text textbox-prompt validatebox-invalid\"   min=\"1\" max=\"65535\" required style=\"width: 60px\"></span><br>").appendTo($("#test1"));

    }

    function  getNamespace() {
        $.ajax({
            url: url+get_namespaces,
            type:"get",
            dataType:"json",
            async:false,
            success: function(data) {

                $.each(data.items,function (i,item) {
                    console.log(item.metadata.name);
                    add_namespace='<span style="width:80px;padding-left: 10px;padding-right: 10px;margin-top: 10px;margin-right:5px;background: yellowgreen" onclick="getResource(this.innerHTML)">'+item.metadata.name+'</span>' ;
                    $("#namespace").append(add_namespace) ;
                })

            },
            error:function(){
                alert("����Namespaceʱ�������쳣!");
            }
            });

    }

    function openWin(src, width, height, showScroll){

        var iWidth = width;
        var iHeight = height;
        var iTop = (window.screen.availHeight - 30 - iHeight) / 2;
        var iLeft = (window.screen.availWidth - 10 - iWidth) / 2;
        var win = window.open(src,"console", "width=" + iWidth + ", height=" + iHeight + ",top=" + iTop + ",left=" + iLeft + ",toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no, status=no,alwaysRaised=yes,depended=yes");

    }
