#!/usr/bin/python  
# -*- coding: utf-8 -*
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

infolist = [{
    "role_title": "“CoSetProxyBlanket”和“CoInitializeSecurity”不应该被使用.",
    "role_desc_en": "CoSetProxyBlanket and CoInitializeSecurity both work to set the permissions context in which the process invoked immediately after is executed. Calling them from within that process is useless because it's to late at that point; the permissions context has already been set.Specifically, these methods are meant to be called from a non-managed code such as a C++ wrapper that then invokes the managed, i.e. C# or VB.NET, code.",
    "role_have_noncompliant_code": "Y",
    "role_noncompliant_code": "\n\n[DllImport(\"ole32.dll\")]\nstatic extern int CoSetProxyBlanket([MarshalAs(UnmanagedType.IUnknown)]object pProxy, uint dwAuthnSvc, uint dwAuthzSvc,\n\t[MarshalAs(UnmanagedType.LPWStr)] string pServerPrincName, uint dwAuthnLevel, uint dwImpLevel, IntPtr pAuthInfo,\n\tuint dwCapabilities);\n\npublic enum RpcAuthnLevel\n{\n\tDefault = 0,\n\tNone = 1,\n\tConnect = 2,\n\tCall = 3,\n\tPkt = 4,\n\tPktIntegrity = 5,\n\tPktPrivacy = 6\n}\n\npublic enum RpcImpLevel\n{\n\tDefault = 0,\n\tAnonymous = 1,\n\tIdentify = 2,\n\tImpersonate = 3,\n\tDelegate = 4\n}\n\npublic enum EoAuthnCap\n{\n\tNone = 0x00,\n\tMutualAuth = 0x01,\n\tStaticCloaking = 0x20,\n\tDynamicCloaking = 0x40,\n\tAnyAuthority = 0x80,\n\tMakeFullSIC = 0x100,\n\tDefault = 0x800,\n\tSecureRefs = 0x02,\n\tAccessControl = 0x04,\n\tAppID = 0x08,\n\tDynamic = 0x10,\n\tRequireFullSIC = 0x200,\n\tAutoImpersonate = 0x400,\n\tNoCustomMarshal = 0x2000,\n\tDisableAAA = 0x1000\n}\n\n[DllImport(\"ole32.dll\")]\npublic static extern int CoInitializeSecurity(IntPtr pVoid, int cAuthSvc, IntPtr asAuthSvc, IntPtr pReserved1,\n\tRpcAuthnLevel level, RpcImpLevel impers, IntPtr pAuthList, EoAuthnCap dwCapabilities, IntPtr pReserved3);\n\nstatic void Main(string[] args)\n{\n\tvar hres1 = CoSetProxyBlanket(null, 0, 0, null, 0, 0, IntPtr.Zero, 0); // Noncompliant\n\n\tvar hres2 = CoInitializeSecurity(IntPtr.Zero, -1, IntPtr.Zero, IntPtr.Zero, RpcAuthnLevel.None,\n\t\tRpcImpLevel.Impersonate, IntPtr.Zero, EoAuthnCap.None, IntPtr.Zero); // Noncompliant\n}\n\n",
    "role_origin_id": "rule_RSPEC-3884",
    "role_id": "S3884",
    "role_desc": "CoSetProxyBlanket和CoInitializeSecurity都可以设置执行后立即调用该进程的权限上下文.在这个过程中召唤他们是无用的，因为那时候迟到了;具体来说，这些方法意在从非托管代码调用，例如C ++包装器，然后调用受管理的.C＃或VB.NET，代码.",
    "role_type": "Vulnerability",
    "role_have_compliant_code": "",
    "role_compliant_code": "",
    "role_level": "BLOCKER",
    "role_title_en": "\"CoSetProxyBlanket\" and \"CoInitializeSecurity\" should not be used"
},
{
    "role_title": "“IDisposables”应该被处理.",
    "role_desc_en": "When writing managed code, you don't need to worry about allocating or freeing memory: The garbage collector takes care of it. For efficiency reasons, some objects such as Bitmap use unmanaged memory, enabling for example the use of pointer arithmetic. Such objects have potentially huge unmanaged memory footprints, but will have tiny managed ones. Unfortunately, the garbage collector only sees the tiny managed footprint, and fails to reclaim the unmanaged memory (by calling Bitmap's finalizer method) in a timely fashion. Moreover, memory is not the only system resource which needs to be managed in a timely fashion: The operating system can only handle having so many file descriptors (e.g. FileStream) or sockets (e.g. WebClient) open at any given time. Therefore, it is important to Dispose of them as soon as they are no longer needed, rather than relying on the garbage collector to call these objects' finalizers at some nondeterministic point in the future.This rule tracks private fields and local variables of the following IDisposable types, which are never disposed, closed, aliased, returned, or passed to other methods.which are either instantiated directly using the new operator, or using one of the following factory methods:on both private fields and local variables.",
    "role_have_noncompliant_code": "Y",
    "role_noncompliant_code": "\n\npublic class ResourceHolder \n{\n  private FileStream fs; // Noncompliant; Dispose or Close are never called\n\n  public void OpenResource(string path)\n  {\n    this.fs = new FileStream(path, FileMode.Open);\n  }\n\n  public void WriteToFile(string path, string text)\n  {\n    var fs = new FileStream(path, FileMode.Open); // Noncompliant\n    var bytes = Encoding.UTF8.GetBytes(text);\n    fs.Write(bytes, 0, bytes.Length);\n  }\n}\n\n",
    "role_origin_id": "rule_RSPEC-2930",
    "role_id": "S2930",
    "role_desc": "编写托管代码时，您不必担心分配或释放内存：垃圾回收器负责处理.出于效率的原因，一些诸如Bitmap的对象使用非托管内存，例如使用指针算术.这样的对象具有潜在的巨大的非管理内存占用空间，但将具有微小的管理内存.不幸的是，垃圾收集器只能看到微小的管理足迹，并且无法及时收回非托管内存（通过调用Bitmap的终结器方法）.此外，内存不是需要及时管理的唯一系统资源：操作系统只能处理具有如此多的文件描述符（e.G.FileStream）或套接字（e.G.WebClient）在任何给定的时间打开.因此，重要的是一旦不再需要处理它们，而不是依靠垃圾收集器在将来的某个非确定性点将这些对象的终止者称为“非确定性”.此规则跟踪以下IDisposable类型的私有字段和局部变量，这些类型不会被处理，关闭，别名，返回或传递给其他方法.它们可以直接使用新的运算符进行实例化，也可以使用以下工厂方法之一：.在私有字段和局部变量上.",
    "role_type": "Bug",
    "role_have_compliant_code": "Y",
    "role_compliant_code": "\n\npublic class ResourceHolder : IDisposable\n{\n  private FileStream fs;\n\n  public void OpenResource(string path)\n  {\n    this.fs = new FileStream(path, FileMode.Open);\n  }\n\n  public void Dispose() \n  {\n    this.fs.Dispose();\n  }\n\n  public void WriteToFile(string path, string text)\n  {\n    using (var fs = new FileStream(path, FileMode.Open))\n    {\n      var bytes = Encoding.UTF8.GetBytes(text);\n      fs.Write(bytes, 0, bytes.Length);\n    }\n  }\n}\n\n",
    "role_level": "BLOCKER",
    "role_title_en": "\"IDisposables\" should be disposed"
},
{
    "role_title": "“的SafeHandle.DangerousGetHandle“不应该被调用.",
    "role_desc_en": "Not surprisingly, the SafeHandle.DangerousGetHandle method is dangerous. That's because it may not return a valid handle. Using it can lead to leaks and vulnerabilities. While it is possible to use the method successfully, it's extremely difficult to do correctly, so the method should simply be avoided altogether.",
    "role_have_noncompliant_code": "Y",
    "role_noncompliant_code": "\n\nstatic void Main(string[] args)\n{\n    System.Reflection.FieldInfo fieldInfo = ...;\n    SafeHandle handle = (SafeHandle)fieldInfo.GetValue(rKey);\n    IntPtr dangerousHandle = handle.DangerousGetHandle();  // Noncompliant\n}\n\n",
    "role_origin_id": "rule_RSPEC-3869",
    "role_id": "S3869",
    "role_desc": "不奇怪的是，SafeHandle.DangerousGetHandle方法是危险的.这是因为它可能不会返回有效的句柄.使用它可能会导致泄漏和漏洞.虽然可以成功使用该方法，但是很难正确执行，所以该方法应该完全避免.",
    "role_type": "Bug",
    "role_have_compliant_code": "",
    "role_compliant_code": "",
    "role_level": "BLOCKER",
    "role_title_en": "\"SafeHandle.DangerousGetHandle\" should not be called"
}]


json.loads(infolist)

print json.loads(infolist)