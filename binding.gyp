{
  "includes": [ "deps/common-sqlite.gypi" ],
  "variables": {
      "sqlite%":"sqlcipher_lib",
      "sqlite_libname%":"sqlcipher",
      "openssl_libname%":"crypto"
  },
  "targets": [
    {
      "target_name": "<(module_name)",
      "include_dirs": ["<!(node -e \"require('nan')\")"],
      "conditions": [
        ["sqlite != 'internal'", {
            "include_dirs": [ "<(module_root_dir)/<(sqlite)/include", "<(module_root_dir)/<(sqlite)/include/sqlcipher", "<(module_root_dir)/<(sqlite)/include/openssl" ],
            "libraries": [
               "-l<(sqlite_libname)",
	       "-l<(openssl_libname)"
            ],
            "conditions": [ [ "OS=='linux'", {"libraries+":["-Wl,-rpath=<(module_root_dir)/<@(sqlite)/lib"]} ] ],
            "conditions": [ [ "OS!='win'", {"libraries+":["-l<(openssl_libname)", "-L<(module_root_dir)/<@(sqlite)/lib"]} ] ],
	    "conditions": [ [ "OS=='win'", {"libraries+":[ "-lmsvcrt", "crypt32.lib", "ws2_32.lib" ] } ] ],
            'msvs_settings': {
              'VCLinkerTool': {
                'AdditionalLibraryDirectories': [
                  '<(module_root_dir)/<(sqlite)/lib'
                ],
		'IgnoreDefaultLibraryNames': [
                  '<(openssl_libname).lib',
                  'crypt32.lib',
                  'ws2_32.lib'
		],
              },
            }
        },
        {
            "dependencies": [
              "deps/sqlite3.gyp:sqlite3"
            ]
        }
        ]
      ],
      "sources": [
        "src/database.cc",
        "src/node_sqlite3.cc",
        "src/statement.cc"
      ]
    },
    {
      "target_name": "action_after_build",
      "type": "none",
      "dependencies": [ "<(module_name)" ],
      "copies": [
          {
            "files": [ "<(PRODUCT_DIR)/<(module_name).node" ],
            "destination": "<(module_path)"
          }
      ]
    }
  ]
}
