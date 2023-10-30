AWS.config.region = 'YOUR_REGION';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: 'YOUR_IDENTITY_POOL_ID'
});

// 创建Cognito身份验证提供者对象
var cognitoProvider = new AWS.CognitoIdentityServiceProvider();

// 处理登录逻辑
submitBtn.onclick = function() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  var params = {
    AuthFlow: 'USER_PASSWORD_AUTH',
    ClientId: 'YOUR_APP_CLIENT_ID',
    UserPoolId: 'YOUR_USER_POOL_ID',
    AuthParameters: {
      USERNAME: username,
      PASSWORD: password
    }
  };

  cognitoProvider.initiateAuth(params, function(err, data) {
    if (err) {
      console.log(err);
    } else {
      // 登录成功，执行自定义操作
      console.log(data);
      modal.style.display = "none";
    }
  });
}