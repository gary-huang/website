from django.conf.urls import url
from django.contrib import admin


# class CustomAdminSite(admin.AdminSite):
#     def get_urls(self):
#         urls = super(CustomAdminSite, self).get_urls()
#         custom_urls = [
#             url(r'desired/path$', self.admin_view(organization_admin.preview), name="preview"),
#         ]
#         return urls + custom_urls
#
#
# class TemplateAdmin(admin.ModelAdmin):
#     change_form_template = 'admin/preview_template.html'
#
# custom_admin_site.register(models.Template, TemplateAdmin)
