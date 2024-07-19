import sys
import mysql.connector
from mysql.connector import Error
from pprint import pprint
import os
# import codegenerator.laravel_11
from codegenerator.laravel_11 import laravel_object_and_file_names
from codegenerator.laravel_11 import column_info
from codegenerator.laravel_11 import model_utilities
from codegenerator.laravel_11.templates import web_controller
from codegenerator.laravel_11.templates import factory
from codegenerator.laravel_11.templates import migration
from codegenerator.laravel_11.templates import model
from codegenerator.laravel_11.templates import request
from codegenerator.laravel_11.templates import seeder
from codegenerator.laravel_11.templates import resource
from codegenerator.laravel_11.templates import resource_collection
from codegenerator.laravel_11.templates import test_feature_controller
# from codegenerator.laravel_11.templates import test_unit_controller
from codegenerator.laravel_11.templates import filter
from codegenerator.laravel_11.templates import filter_base_class
from codegenerator.laravel_11.templates import web_routes_authentication_setup
from codegenerator.laravel_11.templates import policy


def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def fetch_table_and_column_info(connection, database):
    data = {}
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(f"select table_name from information_schema.tables where table_schema = '{database}' and table_type='BASE TABLE'")
        tables = cursor.fetchall()


# SELECT DISTINCT KEY_COLUMN_USAGE.TABLE_NAME, KEY_COLUMN_USAGE.COLUMN_NAME
#     FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE (KEY_COLUMN_USAGE.TABLE_NAME = TABLES.TABLE_NAME AND KEY_COLUMN_USAGE.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)

        for table_name in tables:
            cursor.execute(f"""SELECT COLUMNS.COLUMN_NAME, COLUMNS.ORDINAL_POSITION, COLUMNS.IS_NULLABLE, COLUMNS.DATA_TYPE, 
            COLUMNS.NUMERIC_PRECISION, COLUMNS.NUMERIC_SCALE, COLUMNS.CHARACTER_MAXIMUM_LENGTH, COLUMNS.COLUMN_KEY, COLUMNS.COLUMN_TYPE, 
            COLUMNS.EXTRA, COLUMNS.COLUMN_COMMENT, 
            COLUMNS.COLUMN_DEFAULT, KEY_COLUMN_USAGE.TABLE_NAME, KEY_COLUMN_USAGE.COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS LEFT JOIN
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE ON (  KEY_COLUMN_USAGE.TABLE_NAME = COLUMNS.TABLE_NAME 
            AND KEY_COLUMN_USAGE.TABLE_SCHEMA = COLUMNS.TABLE_SCHEMA 
            AND COLUMNS.COLUMN_NAME = KEY_COLUMN_USAGE.COLUMN_NAME  )
            WHERE COLUMNS.TABLE_SCHEMA = '{database}' 
            AND COLUMNS.TABLE_NAME = '{table_name[0]}' 
            ORDER BY COLUMNS.ORDINAL_POSITION""")
            data[table_name[0]] = [
                {
                    'COLUMN_NAME': row[0],
                    'ORDINAL_POSITION': row[1],
                    'IS_NULLABLE': row[2],
                    'DATA_TYPE': row[3],
                    'NUMERIC_PRECISION': row[4],
                    'NUMERIC_SCALE': row[5],
                    'CHARACTER_MAXIMUM_LENGTH': row[6],
                    'COLUMN_KEY': row[7],
                    'COLUMN_TYPE': row[8],
                    'EXTRA': row[9],
                    'COLUMN_COMMENT': row[10],
                    'COLUMN_DEFAULT': row[11],
                    'FK_TABLE':row[12],
                    'FK_COLUMN':row[13]
                }
                for row in cursor.fetchall()
            ]

        cursor.close()
    else:
        print("Failed to fetch table and column info - No connection to MySQL database")
    return data


# def is_base_table(connection, database, table_name):
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT table_type FROM information_schema.tables WHERE table_name = '{table_name}' and table_schema = '{database}'")
#     table_type = cursor.fetchone()[0]
#     cursor.close()
#     return table_type == "BASE TABLE"


def get_input(prompt, default=None):
    result = input(prompt)
    if not result and default is not None:
        return default
    return result


def main():
    default_host = "localhost"
    default_user = "root"
    default_password = "root"
    default_database = "testData"
    completed_tables = []
    default_output_folder_path = 'c:\\projects\\reactGeneratorOutput\\' #os.path.dirname(os.path.realpath(__file__))+'\\output\\'
    default_ignore_tables = ['failed_jobs', 'migrations', 'password_reset_tokens', 'personal_access_tokens', 'users']
    default_ignore_columns = ['id','user_id', 'created_at', 'updated_at', 'deleted_at','createdBy_user_id','lastUpdatedBy_user_id','lastUpdatedByReal_user_id']
    default_cache_system = 'redis'
    default_use_inertia = 'true'

    host = get_input(f"Enter host (IP address or URL)({default_host}): ", default_host)
    user = get_input(f"Enter user ({default_user}): ", default_user)
    password = get_input(f"Enter password ({default_password}): ", default_password)
    database = get_input(f"Enter database name ({default_database}): ", default_database)
    output_folder_path = get_input(f"Enter output folder path ({default_output_folder_path}): ", default_output_folder_path)
    ignore_tables = default_ignore_tables #get_input(f"Comma separated list of tables to ignore ({', '.join(default_ignore_tables)}): ", default_ignore_tables)
    ignore_columns = default_ignore_columns # get_input(f"Comma separated list of columns to ignore ({', '.join(default_output_folder_path)}): ", default_output_folder_path)
    # cache_system = get_input(f"Enter cache type [none|redis|memcached|dynamodb]- ({default_cache_system}): ", default_cache_system)
    # use_inertia = get_input(f"Use Inertia ({default_use_inertia}): ", default_use_inertia)


    connection = connect_to_database(host, user, password, database)
    data = fetch_table_and_column_info(connection, database)

    for table, columns in data.items():
        if table in ignore_tables:
            continue
        print(f"Writing Laravel PHP files for table '{table}' to {output_folder_path}")
        # pprint(columns)
        # sys.exit(0)
        #is_actual_table = is_base_table(connection, database, table)
        ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table, True, 'redis' )
        ci = column_info.ColumnInfo(columns, ignore_columns)

        # write the web controller file
        web_controller_file_content = web_controller.get_web_controller_file_content(ln, ci)
        file_path = output_folder_path + ln.web_controller_file_path
        file_name = ln.web_controller_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(web_controller_file_content)

        #if is_actual_table :
            # write the factory file
        factory_file_content = factory.get_factory_file_content(ln, ci)
        file_path = output_folder_path + ln.factory_file_path
        file_name = ln.factory_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(factory_file_content)

        #     write the migration file
        migration_file_content = migration.get_migration_file_content(ln, ci)
        file_path = output_folder_path + ln.migration_file_path
        file_name = ln.migration_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(migration_file_content)

        #     write the seeder file
        seeder_file_content = seeder.get_seeder_file_content(ln, ci)
        file_path = output_folder_path + ln.seeder_file_path
        file_name = ln.seeder_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(seeder_file_content)

        #     write the model file
        belongs_to_list = model_utilities.belongs_to(connection, table)
        has_many_list = model_utilities.has_many(connection, table)
        has_many_through_list = model_utilities.has_many_through(connection, table, ignore_columns)
        model_file_content = model.get_model_file_content(ln, ci, belongs_to_list, has_many_list, has_many_through_list)
        file_path = output_folder_path + ln.model_file_path
        file_name = ln.model_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(model_file_content)

        #     write the policy file
        # policy_file_content = policy.get_policy_file_content(ln, ci)
        # file_path = output_folder_path + ln.policy_file_path
        # file_name = ln.policy_file_name
        # os.makedirs(file_path, exist_ok=True)
        # with open(os.path.join(file_path, file_name), 'w') as file:
        #     file.write(policy_file_content)

        #     write the request file
        request_file_content = request.get_request_file_content(ln, ci)
        file_path = output_folder_path + ln.request_file_path
        file_name = ln.request_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(request_file_content)

        #     write the resource file
        resource_file_content = resource.get_resource_file_content(ln, ci)
        file_path = output_folder_path + ln.resource_file_path
        file_name = ln.resource_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(resource_file_content)

        #     write the resource collection file
        # resource_collection_file_content = resource_collection.get_resource_collection_file_content(ln, ci)
        # file_path = output_folder_path + ln.resource_collection_file_path
        # file_name = ln.resource_collection_file_name
        # os.makedirs(file_path, exist_ok=True)
        # with open(os.path.join(file_path, file_name), 'w') as file:
        #     file.write(resource_collection_file_content)

        #if is_actual_table:
        #     write the controller feature test file
        controller_test_file_content = test_feature_controller.get_controller_test_file_content(ln, ci)
        file_path = output_folder_path + ln.test_feature_controller_file_path
        file_name = ln.test_feature_controller_file_name
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_name), 'w') as file:
            file.write(controller_test_file_content)

        #     write the controller unit test file
        # unit_test_file_content = test_unit_controller.get_unit_test_file_content(ln, ci)
        # file_path = output_folder_path + ln.test_unit_file_path
        # file_name = ln.test_unit_file_name
        # os.makedirs(file_path, exist_ok=True)
        # with open(os.path.join(file_path, file_name), 'w') as file:
        #     file.write(unit_test_file_content)

        #     write the filter file
        # filter_file_content = filter.get_filter_file_content(ln, ci)
        # file_path = output_folder_path + ln.filter_file_path
        # file_name = ln.filter_file_name
        # os.makedirs(file_path, exist_ok=True)
        # with open(os.path.join(file_path, file_name), 'w') as file:
        #     file.write(filter_file_content)

        completed_tables.append(table)

    print('\n\nAdd following code to the database\\seeders\\DatabaseSeeders class [in the run() method]\n\n')
    for table in completed_tables:
        # is_actual_table = is_base_table(connection, database, table)
        # if is_actual_table :
        ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table, True, 'redis')
        print(f"        $this->call({ln.model_class_name}TableSeeder::class);")

    # print("\n\n\nAdd following routes to the routes\\api.php [in the run() method]\n\n")
    # for table in completed_tables:
    #     ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table)
    #     print(f"    Route::get('{ln.lcp}', ['as'=>'{ln.lcp}.index', 'uses'=>'{ln.controller_class_name}@index');")
    #     print(f"    Route::post('{ln.lcp}', '{ln.controller_class_name}@store');")
    #     print(f"    Route::get('{ln.lcp}/{{id}}', '{ln.controller_class_name}@show');")
    #     print(f"    Route::put('{ln.lcp}/{{id}}', '{ln.controller_class_name}@update');")
    #     print(f"    Route::delete('{ln.lcp}/{{id}}', '{ln.controller_class_name}@destroy');")
    #     print(f"    Route::get('{ln.lcp}/quick-list', '{ln.controller_class_name}@getQuicklist');")
    #     print('')

    # print("\n\n\nWriting the routes/api_generated.php file - be sure to include this in routes/api.php file\n\n")
    # api_include_content = '<?php \n\n'
    # api_include_content += 'use App\\Http\\Controllers\\API; \n\n'
    # api_include_content += "Route::group(['namespace'=>'App\\Http\\Controllers\\API', 'middleware' => 'auth:sanctum'], function()\n{\n\n"
    # for table in completed_tables:
    #     is_actual_table = is_base_table(connection, database, table)
    #     ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table, is_actual_table, cache_system)
    #     if is_actual_table:
    #         api_include_content += f"Route::apiResource('{ln.lctn}', API\\{ln.api_controller_class_name}::class);\n"
    #     else:
    #         api_include_content += f"Route::get('{ln.lctn}', [API\\{ln.api_controller_class_name}::class, 'index'])->name('{ln.lctn}');\n"
    #     api_include_content += f"Route::get('{ln.lctn}-quicklist', [API\\{ln.api_controller_class_name}::class, 'getQuickList'])->name('{ln.lctn}-quicklist');\n"
    #     api_include_content += f"//Route::post('{ln.lctn}-bulkstore', [API\\{ln.api_controller_class_name}::class, 'bulkStore'])->name('{ln.lctn}-bulkstore');\n\n"
    # api_include_content += "});\n\n"
    # file_path = output_folder_path + ln.api_routes_file_path
    # file_name = ln.api_routes_file_name
    # os.makedirs(file_path, exist_ok=True)
    # with open(os.path.join(file_path, file_name), 'w') as file:
    #     file.write(api_include_content)

    # write the base api filter
    # base_filter_content = filter_base_class.get_filter_base_class()
    # file_path = output_folder_path + ln.base_filter_class_file_path
    # file_name = ln.base_filter_class_file_name
    # os.makedirs(file_path, exist_ok=True)
    # with open(os.path.join(file_path, file_name), 'w') as file:
    #     file.write(base_filter_content)

    # write the web routes authentication setup code
    # web_routes_authentication_setup_content = web_routes_authentication_setup.get_web_routes_authentication_setup()
    # file_path = output_folder_path + ln.web_routes_authentication_setup_file_path
    # file_name = ln.web_routes_authentication_setup_file_name
    # os.makedirs(file_path, exist_ok=True)
    # with open(os.path.join(file_path, file_name), 'w') as file:
    #     file.write(web_routes_authentication_setup_content)

    # print("\n\n\nWriting the routes/web_generated.php file - be sure to include this in routes/web.php file\n\n")
    # web_include_content = ''
    # for table in completed_tables:
    #     ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table)
    #     web_include_content += f"use App\\Http\\Controllers\\{ln.web_controller_class_name};\n"
    # for table in completed_tables:
    #     ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table)
    #     web_include_content += f"Route::resource('{ln.lctn}', [{ln.web_controller_class_name}::class]);\n"
    # file_path = output_folder_path + ln.web_routes_file_path
    # file_name = ln.web_routes_file_name
    # os.makedirs(file_path, exist_ok=True)
    # with open(os.path.join(file_path, file_name), 'w') as file:
    #     file.write(web_include_content)

    # print('route include files written to ' + os.path.join(file_path, file_name))

    print("""Remember to include the following code in the app/Http/middleware/HandleInertiaRequest file share function:
                'flash' => [
                'message' => $request->session()->get('message'),
            ]""")

    print("""Remember to remove the data envelope from Laravel by going to the AppServiceProvider.php 
    add 
        use Illuminate\Http\Resources\Json\JsonResource; 
    to the top and in the boot function add the line
        JsonResource::withoutWrapping();
    """)

    if connection is not None:
        connection.close()

    print('\n\nDone')

    sys.exit(0)


if __name__ == "__main__":
    main()
