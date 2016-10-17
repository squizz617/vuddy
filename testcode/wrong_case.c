void module_layout(struct module *mod,
                   struct modversion_info *ver,
                   struct kernel_param *kp,
                   struct kernel_symbol *ks,
		   struct tracepoint * const *tp) // cannot identify "struct tracepoint * const *tp" as function argument
{
}

void func(void)
{
	int a0[10];
	int a1[10][10]; // cannot identify two-dimensional array (multi-dimensional array?)
	return;
}
