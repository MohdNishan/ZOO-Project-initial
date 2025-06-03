#include <iostream>
#include <string>
#include <cstdio>

extern "C" {
    extern int main_conf_read_parse();
    extern FILE* main_conf_read_in;
}

int loadLocalCfg(const std::string& filename) {
    FILE* file = fopen(filename.c_str(), "r");
    if (!file) {
        std::cerr << "Could not open config file: " << filename << std::endl;
        return 1;
    }

    main_conf_read_in = file;

    if (main_conf_read_parse() != 0) {
        std::cerr << "Error parsing config file: " << filename << std::endl;
        fclose(file);
        return 1;
    }

    fclose(file);
    return 0;
}
