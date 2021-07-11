using System;
using System.IO;
using System.IO.Compression;
using System.Reflection;


//var rand = new Random();

//var modelFile = new byte[10000];
//var labelFile = new byte[1000];

//rand.NextBytes(modelFile);
//rand.NextBytes(labelFile);

using (var stream = new MemoryStream())
{
    using (var archive = new ZipArchive(stream, ZipArchiveMode.Create, true))
    {
        var testEntry = archive.CreateEntry("test.txt");
        using var testEntryStream = testEntry.Open();
        var dataStream = File.OpenRead("Data.txt");
        dataStream.CopyTo(testEntryStream);
    }
    using var resultStream = new FileStream("abc.zip", FileMode.Create);
    stream.Seek(0, SeekOrigin.Begin);
    stream.CopyTo(resultStream);
}