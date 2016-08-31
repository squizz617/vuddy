static inline int handle_dots(struct nameidata *nd, int type)
{
	if (type == LAST_DOTDOT) {
		if (nd->flags & LOOKUP_RCU) {
			if (follow_dotdot_rcu(nd))
				return -ECHILD;
		} else
			follow_dotdot(nd);
	}
	return 0;
}
