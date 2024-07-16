from codegenerator.laravel_11 import utilities
import datetime


class LaravelObjectAndFileNames:
    def __init__(self, table_name, is_table, cache):
        today = datetime.datetime.today()
        current_date = today.strftime('%Y_%m_%d')

        self.is_table = is_table
        self.cache = cache

        self.cfs = utilities.cap_first_single(table_name)
        self.lcs = utilities.lower_case_single(table_name)
        self.lcp = utilities.lower_case_plural(table_name)
        self.cfp = utilities.cap_first_plural(table_name)
        self.tn = table_name
        self.lctn = table_name.lower()

        self.web_controller_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Controller'
        self.web_controller_file_path = 'app/Http/Controllers/'
        self.web_controller_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Controller.php'

        self.api_controller_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'ApiController'
        self.api_controller_file_path = 'app/Http/Controllers/API/'
        self.api_controller_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'ApiController.php'

        self.model_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))
        self.lower_case_model_class_name = self.model_class_name.lower()
        self.model_file_path = 'app/Models/'
        self.model_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'.php'

        self.policy_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Policy'
        self.policy_file_path = 'app/Policies/'
        self.policy_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Policy.php'

        self.request_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Request'
        self.request_file_path = 'app/Http/Requests/'
        self.request_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Request.php'

        self.seeder_file_path = 'database/seeders/'
        self.seeder_file_name = utilities.any_case_to_pascal_case(utilities.plural(table_name))+'TableSeeder.php'
        self.seeder_class_name = utilities.any_case_to_pascal_case(utilities.plural(table_name))+'TableSeeder'

        self.factory_file_path = 'database/factories/'
        self.factory_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Factory.php'
        self.factory_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Factory'

        self.test_feature_controller_file_path = 'tests/Feature/'
        self.test_feature_controller_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'ControllerTest.php'
        self.test_feature_controller_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'ControllerTest'

        self.test_unit_file_path = 'tests/Unit/'
        self.test_unit_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'UnitTest.php'
        self.test_unit_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'UnitTest'

        self.migration_file_path = 'database/migrations/'
        self.migration_file_name = current_date+'_create_'+utilities.any_case_to_pascal_case(utilities.singular(table_name))+'_table.php'
        self.migration_class_name = 'Create'+utilities.any_case_to_pascal_case(utilities.plural(table_name))+'Table'

        self.resource_collection_file_path = 'app/Http/Resources/'
        self.resource_collection_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Collection.php'
        self.resource_collection_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Collection'

        self.resource_file_path = 'app/Http/Resources/'
        self.resource_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Resource.php'
        self.resource_class_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Resource'

        self.api_routes_file_path = 'routes/'
        self.api_routes_file_name = 'api_routes_generated.php'

        self.web_routes_file_path = 'routes'
        self.web_routes_file_name = 'web_routes_generated.php'

        self.base_filter_class_file_path = 'app/Filters/'
        self.base_filter_class_file_name = 'ApiFilter.php'

        self.web_routes_authentication_setup_file_path = 'routes/'
        self.web_routes_authentication_setup_file_name = 'web_routes_authentication_setup.php'

        self.filter_file_path = 'app/Filters/'
        self.filter_file_name = utilities.any_case_to_pascal_case(table_name)+'Filter.php'
        self.filter_class_name = utilities.any_case_to_pascal_case(table_name)+'Filter'

        # self.vue_page_path = 'resources/js/Pages/'
        # self.vue_page_file_name = utilities.cap_first_plural(table_name)+'.vue'
        #
        # self.vue_store_path = 'resources/js/Stores/'
        # self.vue_store_file_name = utilities.any_case_to_pascal_case(utilities.singular(table_name))+'Store.ts'
        #
        # self.vue_component_path = 'resources/js/Components/'+utilities.lower_case_single(table_name)+'/'
        # self.vue_component_search_file_name = utilities.cap_first_plural(table_name)+'Search.vue'
        # self.vue_component_search_file_name = utilities.cap_first_plural(table_name)+'DataTable.vue'
        # self.vue_component_search_file_name = utilities.cap_first_plural(table_name)+'AddEditReadModal.vue'
        # self.vue_component_search_file_name = utilities.cap_first_plural(table_name)+'FkDataTable.vue'
        # self.vue_component_search_file_name = utilities.cap_first_plural(table_name)+'SingleSelectInput.vue'
        # self.vue_component_search_file_name = utilities.cap_first_plural(table_name)+'MultiSelectInput.vue'
