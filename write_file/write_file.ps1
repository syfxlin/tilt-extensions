$Code = @"
using System;
using System.IO;
using System.Text;

namespace PSLib {
    public static class WriteFile {
        public static void Write() {
            string filename = Environment.GetEnvironmentVariable("FILENAME");
            string contents = Environment.GetEnvironmentVariable("CONTENTS");
            File.WriteAllText(filename, contents);
        }
    }
}
"@

Add-Type -TypeDefinition $Code -Language CSharp

[PSLib.WriteFile]::Write()