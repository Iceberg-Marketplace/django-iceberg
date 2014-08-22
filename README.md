django-iceberg
==============
A Django app for [Iceberg-Marketplace](http://www.iceberg-marketplace.com).

## Installation

    $ pip install git+https://github.com/Iceberg-Marketplace/django-iceberg.git#egg=django_iceberg
    
## Setup

Add django_iceberg in your INSTALLED_APPS.  

    INSTALLED_APPS = [
		...
    	'django_iceberg',
	]
	

Be sure you have the **django.core.context_processors.request** context processor.


	TEMPLATE_CONTEXT_PROCESSORS = [
		..
    	"django.core.context_processors.request"
	]



## Use
### TemplateTags
This application give access to 2 templates tags: 

* The **iceberg_javascript_sdk** tag that will add the Iceberg JavaScript SDK on the page.
* The **iceberg_sso** tag that will add User infos on the page to allows further calls to the Iceberg API.

#### Add the templatetags to your pages


	{% load iceberg %} {# At the top of the page #}
	
	{% iceberg_javascript_sdk %} {# Before the closing head tag #}
	{% iceberg_sso %} {# Before the closing body tag #}
   






