
#include <math.h>
#include "common.h"
//#include "test.h"

si*	g_psi_foo;
ull	g_ull_bar;
db	g_adb_hoge[10];
vd*	g_pvd_piyo;
us*	g_apus_fuga[10];

int g_int_hage;

si fl_calc(fl a_fl_arg0, db* a_pdb_arg1, si* a_apsi_arr[]);

typedef struct {
	fl fl_a;
	db db_b;
	int i;
} st_a;

st_a g_test;
st_a st_test;
st_a g_st_test;

typedef enum {
	a,
	b,
	c,
} en_a;

en_a g_test2;
en_a en_test2;
en_a g_en_test2;

fl fl_calc(fl a_fl_arg0, db* a_pdb_arg1, si* a_apsi_arr[])
{
	vd* l_pvd_local = g_pvd_piyo;
	si l_si_foo;
	++l_si_foo;
	
	static unsigned int hoge;
	static int signed hoge2;
	long long a;
	void* b;
	
	st_a l_a;
	st_a st_aa;
	st_a l_st_a;
	
	en_a l_b;
	en_a en_b;
	en_a l_en_b;
	
	float f = sinf(1.0f);
	fl l_f;
	fl fl_f;
	fl l_fl_f;
	
	double d;
	db l_d;
	db db_d;
	db l_db_d;
	
	
}

vd vd_test(
	st_a a_a, st_a st_aa, st_a a_st_a,
	en_a a_b, en_a en_b, en_a a_en_b
	);

