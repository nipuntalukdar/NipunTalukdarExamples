package gopipe

type Executor interface {
	Execute(map[string]interface{})
	AddCollector(Collector)
	AddIdentity(int)
}
