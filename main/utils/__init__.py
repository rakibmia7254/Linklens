from nanoid import generate
import user_agents

def generate_custom_alias():
    return generate(size=6)


def get_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_agent_parser = user_agents.parse(user_agent)
    return {
        'browser': user_agent_parser.browser.family,
        'os': user_agent_parser.os.family,
        'device': user_agent_parser.device.family,
        'country': request.META.get('HTTP_CF_IPCOUNTRY', ''),
    }

def get_ipinfo(request):
    # Get the visitor's real IP address if behind a proxy
    visitor_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if visitor_ip:
        # X-Forwarded-For header is a comma-separated list; the first is the real IP
        visitor_ip = visitor_ip.split(',')[0].strip()
    else:
        # If no proxy, use REMOTE_ADDR
        visitor_ip = request.META.get('REMOTE_ADDR', None)
    
    # Now `visitor_ip` contains the real IP address
    return visitor_ip
