<script type="text/javascript">
$('.btn-xfollow').click(function(){
    var self = $(this);
    var pk = self.parent().attr('pk');
    var url = '{% url feed_xfollow %}';
    var args = {pk:pk};
    $.get(url,args,function(data){
        var ret = data.ret;
        if (ret == 'ok') {
            self.replaceWith(data.html);
        } else {
            alert(data.msg);
        }
    })
});
</script>
