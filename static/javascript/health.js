
//window.open("{% url 'current_patient' %}")
//(screen.center);

/*alert(screen.height/2 + "," + screen.width/2)
alert(screen.height+","+screen.width)
alert(window.innerHeight/2 + "," + window.innerWidth)*/


function checker(){
    //Getting all the variables if (error == true){
     //y=document.getElementById('pre');
    //node = document.CreateElement('p');
    //node = document.CreateTextNode("You have left some fields blank or your entry was not a number ");
    //node.appendChild(textnode);
   // y.appendChild("pre");


var error;

    x =[];
    var i = 0;
    var c=0;
    for(i; i<=10; i++)
 {
    x[i] =document.getElementsByTagName("input")[i];
        if (isNaN(x[i].value)){
         x[i].value = "";
         x[i].placeholder = "Please enter a number";
        c = c+1;
        }
        else if(x[i].value==""){
        x[i].value = "";
        x[i].placeholder = "You have not entered anything";
        c= c+1;
        }
}

if (c > 2){

    node = document.createElement('p');
    textnode = document.createTextNode("You have left some fields blank or your entry was not a number ");
    node.appendChild(textnode);
    node.setAttribute('id', 'error_')
    y=document.getElementById('pre');
    y.appendChild(node);
   }

   else{
    d = document.getElementById("error_");
    if (d){
    d.remove();}
   }

  }


var menu_on = false;
function dropMenu(){

    if (menu_on==false){
         menu_on  = true;
    }
    else{
         menu_on  = false;
    }

    if (menu_on==true){
        b=document.getElementById("menu");
        b.style.display="block";

        var menu_image=document.getElementById("menu_image");
        //menu_image.src="images/right-arrow.png";
        var src= menu_image.getAttribute("image2");
        menu_image.setAttribute('src',src);

        /*var f = document.getElementsByTagName("body")[0];
        f.style.background="rgb(120, 120, 120)";*/
    }
    else{
        b=document.getElementById("menu");
        b.style.display="none";

        var menu_image=document.getElementById("menu_image");
        //menu_image.src="images/menu.png";
        var src= menu_image.getAttribute("image1");
        menu_image.setAttribute('src',src);
    }

}

//profile menu has the edit profile and logout menus.
var profile_on =false;
function dropProfile(){

    if (profile_on ==false){
        profile_on = true;
    }
    else{
        profile_on = false;
    }

    if (profile_on==true){
        b=document.getElementById("profile_menu");
        b.style.display="block";

        /*var menu_image=document.getElementById("menu_image");
        var src= menu_image.getAttribute("image2");
        menu_image.setAttribute('src',src);*/
    }

    else{
        b=document.getElementById("profile_menu");
        b.style.display="none";
        /* var menu_image=document.getElementById("menu_image");
        var src= menu_image.getAttribute("image1");
        menu_image.setAttribute('src',src);*/
    }

}