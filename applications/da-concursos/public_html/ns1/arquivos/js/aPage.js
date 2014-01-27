$(document).ready(function(){
  url = BASEXJ + "apps,55,5/desabafo?callback=?" ;
  limit = 10;
  offset= 10;
  quantit =  COUNT;

  controle(0, limit, quantit);

  $('.next').click(function(){    
      if(quantit - offset > limit){
        a_page(limit, offset);
        controle(offset, limit, quantit)
        offset = offset + limit;
      }else{
        a_page(limit, offset);
        controle(offset, limit, quantit);

      }
  });
  $('.previous').click(function(){
      if(offset > limit){
        offset = offset - limit;       
        a_page(limit, offset);
        controle(offset, limit, quantit)      
      }else{
        a_page(limit, 0);
        controle(0, limit, quantit);
      }

  })
  function a_page(limit, offset){
      limit = limit;   
      offset = offset;    
      $('.paginator').html("");
      $.getJSON(url,{'limit':limit,'offset':offset}, function(data){
        dic = data['ok']['itens'];
        $.each( dic,function(i){
            var desabafo_parse="";
                desabafo_parse += "<div class=\"mgb-large bbd-cinza1\">";
                desabafo_parse += "      <div class=\"reset-mgT reset-mgB\"><small class=\"mgb-large fcinza-e\"><i class=\"icon-calendar\"><\/i>Publicado: " 
                + dic[i]['publicado_em']+ "<\/small><\/div>";
                desabafo_parse += "      <h3 class=\"fs-18 mgt-small mgb-normal lineH20\"> " +dic[i]['titulo']+ "<\/h3>";
                desabafo_parse += "      <p class=\"mgt-normal mgb-large fcinza-m\">";
                desabafo_parse += "        <i class=\"icon-quote-left fs-30 pull-left\"><\/i> " +dic[i]['descricao']+ "<\/p>";
                desabafo_parse += "      <div>";
                desabafo_parse += "        <blockquote class=\"pull-right\"> " +dic[i]['nome']+ "<\/blockquote>";
                desabafo_parse += "        <div class=\"clearfix\"><\/div>";
                desabafo_parse += "      <\/div>";
                desabafo_parse += "    <\/div>";              
            $('.paginator').append(desabafo_parse)  
        })
      })
  }
  function controle(offset, limit, quantit){
     if(offset + limit > quantit){
        limit = quantit % offset;
     } 
    $('#controle').html("Mostrando " + (offset + 1) + " - " + (parseInt(offset) + parseInt(limit)) +  " de " + quantit + " resultados.");
  }
})