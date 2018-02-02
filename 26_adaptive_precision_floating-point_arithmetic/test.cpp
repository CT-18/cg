#include <stdio.h>
#include <random>
#include <gmp.h>
#include <chrono>
#include <iostream>
#include <cassert>

using namespace std;

int turn_gmp(double ax, double ay, double bx, double by, double cx, double cy)
{
	mpq_t axr;
	mpq_init(axr);
	mpq_set_d(axr, ax);
	mpq_t ayr;
	mpq_init(ayr);
	mpq_set_d(ayr, ay);
	mpq_t bxr;
	mpq_init(bxr);
	mpq_set_d(bxr, bx);
	mpq_t byr;
	mpq_init(byr);
	mpq_set_d(byr, by);
	mpq_t cxr;
	mpq_init(cxr);
	mpq_set_d(cxr, cx);
	mpq_t cyr;
	mpq_init(cyr);
	mpq_set_d(cyr, cy);
	
	mpq_t r1;mpq_init(r1);
	mpq_sub(r1, axr, cxr);
	
	mpq_t r2;mpq_init(r2);
	mpq_sub(r2, byr, cyr);
	
	mpq_t r3;mpq_init(r3);
	mpq_sub(r3, bxr, cxr);
	
	mpq_t r4;mpq_init(r4);
	mpq_sub(r4, ayr, cyr);
	
	mpq_t r5;mpq_init(r5);
	mpq_mul(r5, r1, r2);
	
	mpq_t r6;mpq_init(r6);
	mpq_mul(r6, r3, r4);
	
	mpq_t r7;mpq_init(r7);
	mpq_sub(r7, r5, r6);
	
	int res = mpq_sgn(r7);
	mpq_clear(axr);
	mpq_clear(ayr);
	mpq_clear(bxr);
	mpq_clear(byr);
	mpq_clear(cxr);
	mpq_clear(cyr);
	mpq_clear(r1);
	mpq_clear(r2);
	mpq_clear(r3);
	mpq_clear(r4);
	mpq_clear(r5);
	mpq_clear(r6);
	mpq_clear(r7);
	return res;
}

double sum(double a, double b, double& roundoff)
{
	double res = a + b;
	double bv = res - a;
	double av = res - bv;
	double br = b - bv;
	double ar = a - av;
	roundoff = ar + br;
	return res;
}

void split(double a, size_t s, double& hi, double& lo)
{
	double c = ((1LL << s) + 1LL) * a;
	double ab = c - a;
	hi = c - ab;
	lo = a - hi;
}

double mul(double a, double b, double& roundoff)
{
	double res = a * b;
	size_t s = std::numeric_limits<double>::digits / 2 + std::numeric_limits<double>::digits % 2;
	
	double a_hi, a_lo, b_hi, b_lo;
	split(a, s, a_hi, a_lo);
	split(b, s, b_hi, b_lo);
	
	double e1 = res - (a_hi * b_hi);
	double e2 = e1 - (a_lo * b_hi);
	double e3 = e2 - (b_lo * a_hi);
		
	roundoff = (a_lo * b_lo) - e3;
	return res;
}

template <size_t N> struct grow_expansion_f
{
	static void calc(double const* e, double b, double *r)
	{
		b = sum(*e, b, *r);
		grow_expansion_f<N - 1>::calc(e + 1, b, r + 1);
	}
};

template <> struct grow_expansion_f<0>
{
	static void calc(double const* e, double b, double *r)
	{
		*r = b;
	}
};

template <size_t N1, size_t N2> struct expand_sum_f
{
	static void calc(double const* e, double const* f, double *r)
	{
		grow_expansion_f<N1>::calc(e, *f, r);
		expand_sum_f<N1, N2 - 1>::calc(r + 1, f + 1, r + 1);
	}
};

template <size_t N1> struct expand_sum_f<N1, 0>
{
	static void calc(double const* e, double const* f, double *r)
	{
	}
};

template <size_t N> int sign(double const* e)
{
	return e[N-1] > 0 ? 1 : e[N-1] < 0 ? -1 : sign<N-1>(e);
}

template <> int sign<0>(double const* e)
{
	return 0;
}

int turn_adapt(double ax, double ay, double bx, double by, double cx, double cy)
{
	double sa[12];
	sa[1] = mul(ax, by, sa[0]);
	sa[3] = mul(-cx, by, sa[2]);
	sa[5] = mul(ax, -cy, sa[4]);
	sa[7] = mul(-bx, ay, sa[6]);
	sa[9] = mul(cx, ay, sa[8]);
	sa[11] = mul(bx, cy, sa[10]);
	
	double sb[12];
	expand_sum_f<2, 2>::calc(sa + 0, sa + 2, sb);
	expand_sum_f<2, 2>::calc(sa + 4, sa + 6, sb + 4);
	expand_sum_f<2, 2>::calc(sa + 8, sa + 10, sb + 8);
	
	double sc[8];
	expand_sum_f<4, 4>::calc(sb, sb + 4, sc);
	
	double sd[12];
	expand_sum_f<8, 4>::calc(sc, sb + 8, sd);
	
	return sign<12>(sd);
}

void test_correctness()
{
	random_device r;
	default_random_engine e(r());
	uniform_real_distribution<> d(-100000, 100000);
	for (int i = 0; i < 1000000; i++)
	{
		double ax = d(e);
		double ay = d(e);
		double bx = d(e);
		double by = d(e);
		double cx = d(e);
		double cy = d(e);
		assert(turn_gmp(ax, ay, bx, by, cx, cy) == turn_adapt(ax, ay, bx, by, cx, cy));
	}
}


int main()
{
	test_correctness();	
	
	random_device r;
	default_random_engine e(r());
	uniform_real_distribution<> d(-100000, 100000);
	int ans;
	
	auto start = chrono::system_clock::now();
	for (int i = 0; i < 1000000; i++)
	{
		ans = turn_gmp(d(e), d(e), d(e), d(e), d(e), d(e));
	}
	cout << "1000000 turns by gmp " << std::chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now() - start).count() << " ms\n";
	
	start = chrono::system_clock::now();
	for (int i = 0; i < 1000000; i++)
	{
		ans = turn_adapt(d(e), d(e), d(e), d(e), d(e), d(e));
	}
	cout << "1000000 turns by adaptive arithmetic " << std::chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now() - start).count() << " ms\n";
	
}
