from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    # set values for `site_header`, `site_title`, `index_title` etc.
    site_header = 'Custom Admin Site'
    index_template = 'admin/base_site.html'
    

   


custom_admin_site = CustomAdminSite(name='admin')