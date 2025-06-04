#include <gtest/gtest.h>
#include <string>
#include "sqlapi.h"
#define USE_AMQP 1
#define META_DB 1

extern "C" {
#include "service.h"
#include "service_internal.h"
}

int loadLocalCfg(const char*);

TEST(ConfigTest, LoadMainCfg) {
    int result = loadLocalCfg("main.cfg");
    EXPECT_EQ(result, 0);
}

maps* loadCfg() {
    maps* pmsConf = createMaps("database");
    pmsConf->content = createMap("dbname", "zoo");
    addToMap(pmsConf->content, "port","5432");
    EXPECT_FALSE(pmsConf->content == NULLMAP);
    addToMap(pmsConf->content, "user","zoo");
    addToMap(pmsConf->content, "password","zoo");
    addToMap(pmsConf->content, "host","192.168.1.5");
    addToMap(pmsConf->content, "type","PG");
    addToMap(pmsConf->content, "schema","public");
    maps* pmsConf1 = createMaps("auth_env");
    pmsConf1->content = createMap("user", "zoo");
    addMapsToMaps(&pmsConf, pmsConf1);
    freeMaps(&pmsConf1);
    free(pmsConf1);
    return pmsConf;
}

TEST(zoo_service_api_test, createMaps) {
    maps* pmsConf = createMaps("database");
    EXPECT_FALSE(pmsConf == NULLMAP);
    EXPECT_TRUE(pmsConf->content == NULLMAP);
    EXPECT_TRUE(pmsConf->child == NULLMAP);
    EXPECT_TRUE(pmsConf->next == NULLMAP);
    freeMaps(&pmsConf);
    free(pmsConf);
}

TEST(zoo_service_api_test, createFullMaps) {
    maps* pmsConf = loadCfg();
    freeMaps(&pmsConf);
    free(pmsConf);
}

TEST(sqlapi_test, init_sql) {
    maps* pmsConf = loadCfg();
    int iMetadb=init_sql(pmsConf);
    EXPECT_EQ(iMetadb, 1);
    //dumpMaps(pmsConf);
    map* pmErrorMessage=getMapFromMaps(pmsConf,"lenv","message");
    if(pmErrorMessage!=NULL){
        ZOO_DEBUG(pmErrorMessage->value);
    }
    close_sql(pmsConf,iMetadb);
    end_sql();
    freeMaps(&pmsConf);
    free(pmsConf);
}

// TEST(sqlapi_test, getUserId) {
//     maps* pmsConf = loadCfg();
//     int iMetadb=init_sql(pmsConf);
//     EXPECT_FALSE(iMetadb == 0);
//     getUserId(pmsConf, iMetadb, pmsConf->content);
//     char* pcaSqlQuery = (char*)malloc(100*sizeof(char));
//     sprintf(pcaSqlQuery, "init_sql: iMetadb=%d", iMetadb);
//     ZOO_DEBUG(pcaSqlQuery);
//     //EXPECT_EQ(iMetadb, 1);
//     free(pcaSqlQuery);
//     close_sql(pmsConf,iMetadb);
//     end_sql();
//     freeMaps(&pmsConf);
//     free(pmsConf);
// }