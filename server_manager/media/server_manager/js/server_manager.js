function refresh_uptime(site_id)
{
	var target = django.jQuery('#uptime_' + site_id);
	django.jQuery.ajax({
        type: 'POST',
        url: '?ajax=true',
        data: {
            site_id: site_id,
            action: 'uptime',
        },
        success: function(data, textStatus, XMLHttpRequest){
            if (data)
            {
            	target.html(data);
            }
            else
            {
            	target.html(SERVER_MANAGER_I18N['uptime']['unknown']);
            }
        },
        error: function(){
        	target.html(SERVER_MANAGER_I18N['uptime']['unknown']);
        },
        dataType: 'json',
    });
	
}

function clear_message(ele_id)
{
	django.jQuery('#' + ele_id).parent().find('.response-message').html('');
}

function handle_timeout(ele)
{
	timeoutid = ele.data('timeout-id');
	if (timeoutid)
	{
		clearTimeout(timeoutid);
	}
	timeoutid = setTimeout("clear_message('" + ele.attr('id') + "')", 5000);
	ele.data('timeout-id', timeoutid);
}

function add_success_message(ele, action)
{
	handle_timeout(ele);
	ele.parent().find('.response-message').html(SERVER_MANAGER_I18N[action]['success']);
	refresh_uptime(ele.parent().find('button.server-manager').attr('value'));
}

function add_error_message(ele, action)
{
	handle_timeout(ele);
	ele.parent().find('.response-message').html(SERVER_MANAGER_I18N[action]['error']);
}

(function($) {
    $(document).ready(function($) {
        // Bind button actions
    	$('button.server-manager').click(function(){
    		var site_id = $(this).attr('value');
    		$(this).attr('disabled', 'disabled');
    		var action = $(this).attr('name');
    		var ele = $(this);
    		$.ajax({
                type: 'POST',
                url: '?ajax=true',
                data: {
                    site_id: site_id,
                    action: action,
                },
                success: function(data, textStatus, XMLHttpRequest){
                	ele.removeAttr('disabled');
                    if (data)
                    {
                    	add_success_message(ele, action);
                    }
                    else
                    {
                    	add_error_message(ele, action);
                    }
                },
                error: function(){
                	ele.removeAttr('disabled');
                	add_error_message(ele, action);
                },
                dataType: 'json',
            });
    	});
    });
})(django.jQuery);
